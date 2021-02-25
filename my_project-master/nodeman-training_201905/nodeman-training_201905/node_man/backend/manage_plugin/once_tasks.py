import base64
import inspect
import json
import posixpath
import re
import time
import os
import traceback

from celery.task import task

from node_man.component.esbclient import client_v2 as client
from node_man.component.exceptions import ComponentCallError, StepFailure
from node_man.constants import StepType, StatusType, JobType
from node_man.models import Job, JobTask, Cloud, ProcControl
from node_man.models import Packages
from node_man.utils.basic import now

Namespace = "nodeman"
IP_pattern = re.compile("((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)")
Target_path_map = {"linux": "/tmp/nodeman_upload/",
                   "windows": "c:\\tmp\\nodeman_upload"
                   }
Account_map = {"linux": "root",
               "windows": "system"}
Config = {}

GSE_TASK_RUNNING = 115
GSE_PROC_RUNNING = 828
GSE_PROC_REGISTERED = 850
GSE_NO_ERROR = 0

GSE_OP_MAP = {
    "START_PLUGIN": 0,
    'STOP_PLUGIN': 1,
    'RELOAD_PLUGIN': 8,
    'RESTART_PLUGIN': 7,
    'DELEGATE_PLUGIN': 3,
    'UNDELEGATE_PLUGIN': 4,
    'UPGRADE_PLUGIN': 7,
    'UPDATE_PLUGIN': 7
}

MAX_RETRY_COUNT = 60


@task()
def manage_process(job_id, **kwargs):
    job = Job.objects.get(id=job_id)
    client.set_bk_supplier_account(job.bk_supplier_account)
    client.set_username(job.creator)

    job_tasks = job.get_job_tasks()

    for task in job_tasks:
        task.update_step(StepType.REGISTER_PROCESS)
        task.update_status(StatusType.RUNNING)

    try:
        register_process(job, job_tasks)
        operate_process(job, job_tasks)
    except ComponentCallError as err:
        job.log(u"Call ESB Error {}".format(err.message))
        job.update_status(StatusType.FAILED)
    except StepFailure as err:
        job.log(err.message)
        job.update_status(StatusType.FAILED)
    except Exception as err:
        job.log(u"Unknown error happened: {}\nTraceback: {}".format(err, traceback.format_exc()))
        job.update_status(StatusType.FAILED)
    update_job_end_time(job)


def register_process(job, job_tasks):
    args = create_operate_proc_args(job, job_tasks)
    job.log("register process with args (display in json here): {}".format(json.dumps(args)))
    response = client.gse.register_proc_info(**args)
    for key in response.keys():
        complete_register(job, key, response.get(key))


def operate_process(job, job_tasks):
    args = create_operate_proc_args(job, job_tasks, need_register=False)
    response = client.gse.operate_proc(**args)
    print "response is:", response
    task_id = response.get("task_id")
    poll_operate_task(job, task_id)


def poll_operate_task(job, task_id):
    kwargs = {
        "namespace": Namespace,
        "task_id": task_id
    }

    retries = 0
    response = client.gse.get_proc_operate_result(**kwargs)
    unfinished_keys = set(response.keys())
    while unfinished_keys:
        print response
        for key in set(unfinished_keys):
            error_code = response.get(key).get('error_code')
            if error_code != GSE_TASK_RUNNING:
                complete_managing_process(job, key, response.get(key))
                unfinished_keys.remove(key)
        if retries > MAX_RETRY_COUNT:
            job.log("Timeout: {} still not finished".format(" ".join(unfinished_keys)))
            break
        response = client.gse.get_proc_operate_result(**kwargs)
        time.sleep(2)
        retries += 1


def update_job_end_time(job):
    job.end_time = now()
    job.save()


def complete_managing_process(job, key, data):
    error_code, error_mssage = [data.get(attr) for attr in ('error_code', 'error_msg')]
    cloud_id, ip = [key.split(":")[i] for i in (0, 2)]
    tasks = JobTask.objects.filter(host__bk_cloud_id=cloud_id, host__inner_ip=ip, job__id=job.id)

    if error_code == GSE_NO_ERROR or error_code == GSE_TASK_RUNNING and job.job_type == JobType.START_PLUGIN:
        step = StepType.OVER_SUCCESS
        status = StatusType.SUCCESS
        log = "{} successfully finished, error_code={}".format(job.job_type, error_code)
    else:
        step = StepType.OVER_FAILED
        status = StatusType.FAILED
        log = "{} failed, error message is: {}".format(job.job_type, error_mssage)
    tasks[0].log(log)
    tasks[0].update_step(step)
    tasks[0].update_status(status)


def complete_register(job, key, data):
    error_code, error_mssage = [data.get(attr) for attr in ('error_code', 'error_msg')]
    cloud_id, ip = [key.split(":")[i] for i in (0, 2)]
    tasks = JobTask.objects.filter(host__bk_cloud_id=cloud_id, host__inner_ip=ip, job__id=job.id)
    if error_code in (GSE_NO_ERROR, GSE_PROC_REGISTERED):
        step = StepType.OPERATE_PROCESS
        status = StatusType.RUNNING
        log = "Register success[{}]".format(error_code)
    else:
        step = StepType.REGISTER_PROCESS
        status = StatusType.FAILED
        log = "Register failed, error message is: {}".format(error_mssage)

    tasks[0].log(log)

    # TODO: move step update action outside
    if job.job_type not in ("UPGRADE_PLUGIN", "UPDATE_PLUGIN"):
        tasks[0].update_step(step)
    tasks[0].update_status(status)


def create_operate_proc_args(job, job_tasks, need_register=True):
    op_type = GSE_OP_MAP.get(job.job_type)
    hosts = map(__get_host_info, job_tasks)

    global_params = json.loads(job.global_params)
    process_name = global_params.get("plugin", {}).get("name", "")

    meta = {
        "namespace": Namespace,
        "name": process_name,
        "labels": {
            "procname": process_name
        }
    }
    result = {"meta": meta, "op_type": op_type, "hosts": hosts}

    if need_register:
        os = job_tasks.first().host.os_type.lower()
        category = global_params.get("plugin", {}).get("category", "")
        try:
            spec = create_spec_args(process_name, category, os)
        except IndexError as err:
            job.log("Control information for '{}' process '{}' in '{}' is missing in DB.".format(
                category, process_name, os))
            job.log("Please reset the configuration.")
            raise StepFailure
        result.update(spec=spec)
    return result


def __get_host_info(task, need_supplier_id=True):
    cloud_id = int(task.host.bk_cloud_id)
    # supplier_id = int(Cloud.objects.filter(bk_cloud_id=cloud_id)[0].bk_supplier_id)
    supplier_id = int(task.host.bk_supplier_id) if task.host.bk_supplier_id else 0
    result = dict(ip=task.host.inner_ip, bk_cloud_id=cloud_id)
    if need_supplier_id:
        result.update(bk_supplier_id=supplier_id)
    return result


def create_spec_args(proc_name, category, os):
    proc_ctrl_info = ProcControl.objects.filter(project=proc_name, os=os)[0]
    linux_plugin_path_mapping = {"official": "plugins/bin",
                                 "external": "external_plugins/{}/bin".format(proc_name),
                                 "scripts": "external_scripts"
                                 }
    win_plugin_path_mapping = {"official": "plugins\\bin",
                               "external": "external_plugins\\{}\\bin".format(proc_name),
                               "scripts": "external_scripts"
                               }
    if os == "windows":
        setup_path = "{}\\{}".format(proc_ctrl_info.install_path, win_plugin_path_mapping.get(category, "plugins\\bin"))
    else:
        setup_path = posixpath.join(proc_ctrl_info.install_path, linux_plugin_path_mapping.get(category, "plugins/bin"))
    return {
        "identity": {
            "proc_name": proc_name,
            "setup_path": setup_path,
            # bug: pid_path must ends with .pid
            "pid_path": proc_ctrl_info.pid_path,
            "user": Account_map.get(os, "root")
        },
        "control": {
            "start_cmd": proc_ctrl_info.start_cmd,
            "stop_cmd": proc_ctrl_info.stop_cmd,
            "restart_cmd": proc_ctrl_info.restart_cmd,
            "reload_cmd": proc_ctrl_info.reload_cmd,
            "kill_cmd": proc_ctrl_info.kill_cmd,
            "version_cmd": proc_ctrl_info.version_cmd,
            "health_cmd": proc_ctrl_info.health_cmd
        },
        "resource": {
            "cpu": 10.0,
            "mem": 10.0,
        },
        "monitor_policy": {
            "auto_type": 1,
        },
    }


@task()
def update_plugin(job_id, **kwargs):
    job = Job.objects.get(id=job_id)
    client.set_bk_supplier_account(job.bk_supplier_account)
    client.set_username(job.creator)

    job_tasks = job.get_job_tasks()

    job.update_status(StatusType.RUNNING)
    job.update_job_step(StepType.UPLOAD_FILE)
    job.log("start to upload file")

    try:
        copy_binary(job, job_tasks)
        update_binary(job, job_tasks)
        restart_plugin(job, job_tasks)
    except ComponentCallError as err:
        job.update_status(StatusType.FAILED)
        job.update_job_step(StepType.OVER_FAILED)
        job.log(u"update plugin failed: {}".format(err.message))
    except Exception as err:
        job.log(u"unknown error happened: {} \n Traceback is: {}".format(err, traceback.format_exc()))
        job.update_status(StatusType.FAILED)
    update_job_end_time(job)


def restart_plugin(job, job_tasks):
    global_params = json.loads(job.global_params)
    no_restart = global_params["option"]["no_restart"]
    if not no_restart:
        job.update_job_step(StepType.RESTART_PROCESS)
        register_process(job, job_tasks)
        operate_process(job, job_tasks)
    else:
        job.update_status(StatusType.SUCCESS)
        job.update_job_step(StepType.OVER_SUCCESS)


def copy_binary(job, job_tasks):
    # for job_task in job_tasks:
    #     job_task.update_status(StatusType.RUNNING)
    #     job_task.update_step(StepType.UPLOAD_FILE)
    #     job_task.log("start to upload file")
    step = inspect.getframeinfo(inspect.currentframe()).function.replace("_", " ")

    return execute_platform_job(job, job_tasks, step)

    # job_instance_id = response['job_instance_id']
    #
    # # for task in job_tasks:
    # #     task.log("copy binary file job submitted, job instance id is: {}".format(job_instance_id))
    # job.log("JJJ, copy binary file job submitted, job instance id is: {}".format(job_instance_id))
    #
    # retry = 0
    # while not client.job.get_job_instance_log({"job_instance_id": job_instance_id, "bk_biz_id": 2})[0]["is_finished"]:
    #     time.sleep(2)
    #     retry += 1
    #     # for task in job_tasks:
    #     #     task.log("copy binary file job not finished, job instance id is: {}".format(job_instance_id))
    #     job.log("JJJ, copy binary file job not finished, job instance id is: {}".format(job_instance_id))
    #     if retry > 60:
    #         job.log("JJJ, copy file failed")
    #         return False
    # else:
    #     logs = client.job.get_job_instance_log({"job_instance_id": job_instance_id, "bk_biz_id": 2})[0]["step_results"][0]["ip_logs"]
    #     for log in logs:
    #         task = job_tasks.filter(host__inner_ip=log['ip'])[0]
    #         task.log(log['log_content'])
    #     return True


def update_binary(job, job_tasks):
    job.update_job_step(StepType.OVERWRITE_FILE)
    job.log("start to update file")
    step = inspect.getframeinfo(inspect.currentframe()).function.replace("_", " ")
    return execute_platform_job(job, job_tasks, step)


def execute_platform_job(job, job_tasks, step):
    args = create_update_plugin_args(job, job_tasks, step)
    response = client.job.execute_platform_job(**args)

    job_instance_id = response['job_instance_id']
    print job_instance_id
    # for task in job_tasks:
    #     task.log("copy binary file job submitted, job instance id is: {}".format(job_instance_id))

    job.log("{} job submitted, job instance id is: {}".format(step, job_instance_id))

    retry = 0
    while not client.job.get_job_instance_log({"job_instance_id": job_instance_id, "bk_biz_id": int(job.bk_biz_id)})[0][
        "is_finished"]:
        time.sleep(2)
        retry += 1
        # for task in job_tasks:
        #     task.log("copy binary file job not finished, job instance id is: {}".format(job_instance_id))
        job.log("{} job not finished, job instance id is: {}".format(step, job_instance_id))
        if retry > MAX_RETRY_COUNT:
            job.log("copy file failed")
            return False
    else:
        logs = client.job.get_job_instance_log({"job_instance_id": job_instance_id,
                                                "bk_biz_id": int(job.bk_biz_id)
                                                })[0]["step_results"][0]["ip_logs"]
        # print logs
        for log in logs:
            task = job_tasks.filter(host__inner_ip=log['ip'])[0]
            task.log(log['log_content'])
        return True


def create_update_plugin_args(job, job_tasks, step="copy binary"):
    global_params = json.loads(job.global_params)
    package = Packages.objects.filter(id=global_params["package"]["id"])[0]
    target_biz_id = job_tasks[0].host.bk_biz_id

    ip_list = [__get_host_info(task, False) for task in job_tasks]
    if step == "copy binary":
        steps = [create_copy_file_step(package, ip_list)]
    elif step == "update binary":
        steps = [create_execute_cmd_step(ip_list, global_params)]
    elif step == "update config":
        steps = [create_update_cfg_step(ip_list, global_params)]
    return {
        "source_bk_biz_id": 2,
        "target_bk_biz_id": target_biz_id,
        "bk_job_id": 7,
        "steps": steps
        # "steps": [copy_file_step]
    }


def create_copy_file_step(package, ip_list):
    # control_info = ProcessControlInfo.objects.filter(module=package.module, project=package.project)[0]
    # target_path = control_info.install_path
    # target_path = "/tmp/"
    source_file = posixpath.join(package.pkg_path, package.pkg_name)
    source_ip = IP_pattern.search(package.location).group()
    source_ip_list = [dict(ip=source_ip, bk_cloud_id=0)]
    target_path = Target_path_map.get(package.os, "linux")
    # print "target_file_path:", target_path
    # print "source_file:", source_file
    result = {
        "file_target_path": target_path,
        "file_source": [
            {
                "files": [source_file],
                "account": "root",
                "ip_list": source_ip_list
            }
        ],
        "ip_list": ip_list,
        "step_id": 20,
        "account": Account_map.get(package.os, "root")  # to be determined
    }
    return result


def create_execute_cmd_step(ip_list, global_params):
    # script_param = "-t official -p /tmp/test -n basereport -f basereport-10.0.1.tgz -m override -u"
    target_path = Target_path_map.get(global_params["package"]["os"], "linux")
    script_param = "-t {category} -p {gse_home} -n {name} -f {package} -z {target} -m {upgrade_type}{keep_config}".format(
        keep_config=" -u" if global_params["option"]["keep_config"] else "",
        category=global_params["plugin"]["category"],
        gse_home=global_params["control"]["install_path"],
        name=global_params["plugin"]["name"],
        package=global_params["package"]["pkg_name"],
        upgrade_type=global_params["upgrade_type"],
        target=target_path
    )
    os_type = global_params["package"]["os"]
    print script_param
    script_map = {"linux": "update_binary.sh",
                  "windows": "update_binary.bat"}
    script_file = script_map[os_type]
    path = os.path.join(os.path.dirname(__file__), script_file)
    with open(path) as fh:
        cmd = fh.read()
        cmd = cmd.decode("utf-8-sig").encode("utf-8")

    result = {
        "script_timeout": 1000,
        "script_param": base64.b64encode(script_param),
        "ip_list": ip_list,
        "script_content": base64.b64encode(cmd),
        "step_id": 19,
        "account": Account_map.get(global_params["package"]["os"], "root"),
        "script_type": 1 if os_type == "linux" else 2
    }
    return result


def update_config(job, job_tasks):
    job.update_job_step(StepType.REPLACE_CONFIG)

    global Config
    configs = json.loads(job.global_params)["configs"]
    step = inspect.getframeinfo(inspect.currentframe()).function.replace("_", " ")
    ## TODO: do not use the poll for the whole job
    for config in configs:
        Config = config
        job.log("start to replace config file for {}".format(Config["inner_ips"]))
        execute_platform_job(job, job_tasks, step)
    job.log("successfully updated config files")


def create_update_cfg_step(ip_list, global_params):
    target_path = Target_path_map.get(global_params["package"].get("os", "linux"), "")
    script_param = "-t {category} -p {gse_home} -n {name} -f {package} -z {target} -m {upgrade_type}".format(
        category=global_params["plugin"]["category"],
        gse_home=global_params["control"]["install_path"],
        name=global_params["plugin"]["name"],
        package=global_params["package"]["pkg_name"],
        upgrade_type=global_params["upgrade_type"],
        target=target_path
    )

    path = os.path.join(os.path.dirname(__file__), "update_cfg.sh")
    with open(path) as fh:
        cmd = fh.read()
    cmd = cmd.replace("THE_CONFIG_CONTENT", base64.b64decode(Config["content"]))

    ip_list = [ip for ip in ip_list if ip["ip"] in Config["inner_ips"]]
    result = {
        "script_timeout": 1000,
        "script_param": base64.b64encode(script_param),
        "ip_list": ip_list,
        "script_content": base64.b64encode(cmd),
        "step_id": 19,
        "account": Account_map.get(global_params["package"]["os"], "root"),
        "script_type": 1
    }
    return result


@task()
def update_plugin_with_config(job_id, **kwargs):
    job = Job.objects.get(id=job_id)
    client.set_bk_supplier_account(job.bk_supplier_account)
    client.set_username(job.creator)
    job_tasks = job.get_job_tasks()

    job.update_status(StatusType.RUNNING)
    job.update_job_step(StepType.UPLOAD_FILE)
    job.log("start to upload file")

    try:
        copy_binary(job, job_tasks)
        update_config(job, job_tasks)
        update_binary(job, job_tasks)
        restart_plugin(job, job_tasks)
    except ComponentCallError as err:
        job.update_status(StatusType.FAILED)
        job.update_job_step(StepType.OVER_FAILED)
        job.log(u"update plugin with config failed: {}".format(err.message))
    except Exception as err:
        job.log(u"unknown error happened: {} \n Traceback is: {}".format(err, traceback.format_exc()))
        job.update_status(StatusType.FAILED)
    finally:
        update_job_end_time(job)
