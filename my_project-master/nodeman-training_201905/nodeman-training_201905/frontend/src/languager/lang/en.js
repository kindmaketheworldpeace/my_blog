/**
 * 英文语言包
 */
export const m = {
    header: {
        title: 'NodeMan',
        node: 'OverView',
        manage: 'AgentSetup',
        examine: 'Healthy',
        schematic: 'MiniDocs'
    },
    search: {
        cluster: 'cluster',
        modules: 'modules',
        changeCloud: 'select cloud area',
        screen: 'query',
        placeholder: 'please choose',
        searchContent: 'search'
    },
    tabControl: {
        allArea: 'ALL',
        directArea: 'DIRECT',
        cloudArea: 'cloud area',
        cloudManag: 'Area Manager',
        copyGood: 'copy selected IP',
        copyBad: 'copy bad status IP',
        addAgent: 'agent',
        addProxy: 'proxy',
        addPagent: 'p-agent',
        importCmdb: 'import from CMDB',
        data: 'no data found'
    },
    addNode: {
        nodeType: 'NODETYPE',
        address: 'IP',
        innerip: 'LAN IP',
        outerip: 'WAN IP',
        please: 'IP:PORT',
        port: 'Port',
        account: 'ACCOUNT',
        verify: 'Auth Method',
        password: 'by password',
        passInfo: 'password',
        passInput: 'input password',
        key: 'by ssh key',
        upload: 'upload key file',
        operat: 'OS',
        operation: 'Operates',
        add: 'add',
        delete: 'del',
        clickStart: 'click to INSTALL',
        progress: 'Install in Progress...',
        addit: 'Import in Progress...'
    },
    check: {
        address: 'IP address can not be empty',
        port: 'SSH port can not be empy',
        account: 'Account can not be empy',
        key: 'Please upload the ssh key file',
        agent: 'Add agent node successfully',
        proxy: 'Add proxy node successfully',
        error: 'Add node failed.',
        legal: 'Port is illegal!',
        ipLegal: 'IP address is illegal!'
    },
    headTab: {
        area: 'AREA NAME',
        status: 'Agent VERSION/STATUS',
        updateTime: 'UPDATE TIME',
        step: 'TASK STATUS'
    },
    operateStep: {
        upgrade: 'upgrade',
        reinstall: 'reinstall',
        uninstall: 'uninstall',
        stop: 'terminate',
        remove: 'remove',
        compile: 'edit'
    },
    addCloud: {
        deleteArea: 'make sure all nodes in this area are removed before delete',
        newCloud: 'new cloud area',
        openCloud: 'Confirm ?',
        cloudPlace: 'area name(<= 64 char)',
        deleteCloud: 'cloud area removed'
    },
    clickBtn: {
        confirm: 'confirm',
        configNow: 'setup',
        cancel: 'cancel',
        save: 'save',
        add: 'add',
        import: 'import',
        continue: 'continue',
        return: 'return',
        update: 'update',
        time: 'timeout',
        timePlace: 'Please enter timeout period in seconds'
    },
    openSlider: {
        stepInfo: 'progress details',
        attention: {
            stepOne: 'User Administrator/system is required for Windows & Windows(Cygwin) OS, otherwise, root is required.',
            stepTwo: 'To install agent, SMB port 445 for Windows, either SSH or SMB port for windows(Cygwin) should be connectable',
            stepThree: 'Proxy and appo(this app) will try to login agent through the corrosponding port mentioned above'
        },
        compileOpear: {
            please: 'IP adress',
            enterPort: 'SSH port',
            enterAct: 'account name',
            reinstall: 'reinstall',
            uninstall: 'uninstall',
            remove: 'remove',
            save: 'save only'
        },
        cmdb: {
            installNum: 'hosts ready for install',
            continue: 'Click [continue] to ignore the above IP to start installation',
            return: 'Click [return] to modify'
        }
    },
    message: {
        comfireOpera: 'are you sure to perform this action ?',
        comfireInfo: 'are you sure to perform this action ?',
        searchCloud: 'cloud area',
        cloudName: 'cloud area name cannot be empty!',
        cloudClash: 'area name conflicts with builtin name !',
        cloudExist: 'area name repeated !',
        cloudSuccess: 'add cloud area succeded !',
        proxy: 'proxy info is editting, are you sure to discard and leave?',
        agent: 'agent info is editting, are you sure to discard and leave?',
        checkInfo: 'No hosts selected',
        taskBegin: 'task started',
        batchTask: 'Batch operation task started',
        task: {
            saveTask: 'saving ...',
            reinstallTask: 'start to re-install',
            uninstallTask: 'start to un-install',
            removeTask: 'start to remove',
            stopTask: 'trying to stop',
            errorTask: 're-install failed, please correct host information',
            checkClash: 'the hosts selected',
            doNot: 'cannot proceed',
            runClash: 'there is a running task on the selected hosts. please un-check it and try again',
            proxyClash: 'the proxy and p-agent nodes cannot be operated simultaneously.'
        },
        batch: {
            upgrade: 'batch upgrade',
            reinstall: 'batch re-install',
            uninstall: 'batch un-install',
            stop: 'batch terminate',
            remove: 'batch removal',
            compile: 'batch edit'
        }
    },
    nginx: {
        info: {
            title: 'Please fill the field with NGINX IP:PORT of BLUEKING server. the package of agent will be downloaded from nginx.',
            pointOne: 'In direct area, packages are downloaded via nginx LAN IP.',
            pointTwo: 'In cloud Area, packages are downloaded via nginx WAN IP. and saved on proxy nodes'
        },
        port: 'NGINX_IP:PORT',
        welcome: 'Welcome to Node Manager, please setup Nginx Server first.',
        configuration: 'Configure NGINX',
        save: 'nginx server info saved successfully',
        configOk: 'setup successfully',
        infokey: 'Please fill all the blanks'
    },
    otherWord: {
        all: 'ALL',
        fuzzy: 'Fuzzy query',
        sureInfo: 'Please correct all information',
        complete: 'Please complete all information',
        business: 'No business found, Please check if CMDB is alive!',
        table: {
            connect: 'Zookeeper port (zk)',
            task: 'GSE Task server (gse_task)',
            data: 'GSE Data server (gse_data)',
            text: 'GSE File server (gse_btsvr)',
            agentListen: 'GSE Agent port (gse_agent)',
            nginxListen: 'Nginx port (nginx)',
            type: 'Port Type',
            opp: 'Service Name',
            instra: 'Remark'
        },
        figure: {
            agentInstall: 'STEPS for Agent installation',
            direaAgent: 'DIRECT connectivy area',
            appoAgent: 'Start a SSH connection to Agent from APPO, download the installation script and execute, then package downloading, Agent installing and starting will be carry out step by step',
            noAgent: 'NON-DIRECT connectivy area',
            appoProxy: 'Start a SSH connection to Proxy from APP, download the installation script, and install Proxy. save p-agent info to temp file and generate new script for p-agent installation',
            job: 'Create a quick script Job task on proxy, execute the script generated on previous step on the Proxy node(p-agent info was paased to script)',
            net: 'Network access strategy',
            agentPort: 'agents in DIRECT area/Proxy: make sure agent/proxy node is able to connnect to the port below of BLUEKING service',
            ssh: 'make sure APPO IS ABLE TO connect Linux/Cygwin Agent by SSH port, Windows Agent by SMB port 139 or 445'
        },
        router: {
            node: 'Overview',
            manag: 'Agent Setup',
            healty: 'Healthy',
            plug: 'Plugin',
            task: 'Tasks'
        }
    },
    addInfo: {
        agent: {
            condition: 'PREREQUISITE',
            add: 'Click + add agent to deploy agent',
            appo: 'APPO (where the nodeman app runs) must be able to login to the Agent machine via SSH',
            zk: 'Agent can access zookeeper',
            opera: 'Linux/Windows/AIX operating systems are supported',
            port: 'Windows server without Cygwin installed must have SMB service(TCP/445) enabled',
            root: 'Only root/Administrator is supported to do it'
        },
        pAgent: {
            app: 'Any proxy node must be able to login to the p-agent via SSH',
            port: "'p-agent can access the Proxy's' port"
        },
        proxy: {
            add: 'First,  add a proxy',
            info: 'Click button +add proxy, input the proxy data, and start the installation',
            status: 'Once Proxy state is ACTIVE(in green), you could add a p-agent node in that area',
            statusInfo: 'Click +add p-agent,  setup p-agent information and  click INSTALL',
            cloud: 'CLOUD AREA: a set of servers, hosts in the same LAN can access each other by LAN IP, and proxy can get ebstalished with gse server by WAN IP',
            linux: 'PROXY must be a CentOS Linux 64-bit OS, at least one IP can be interlinked with the GSE server (ports refer to the instructions in the deployment guide in the top navigation), and fill the WANIP blank with this IP',
            ssh: 'Make sure that appo is accessable through SSH to the Proxy server',
            nginx: 'Make sure the proxy server can access the nginx server',
            root: 'Only root user is supported for installation'
        }
    },
    addSomeInfo: {
        direct: 'Direct Area <-> GSE',
        agentGse: 'Proxy <-> GSE',
        pagentGse: 'P-Agent <-> Proxy',
        source: 'source',
        target: 'target',
        protocol: 'protocol',
        port: 'port(s)',
        usage: 'usage',
        remark: 'remark',
        task: 'for task execution port',
        data: 'for data transmission port',
        bt: 'BT transmission',
        btNone: 'BT transmission, optional',
        query: 'query out configuration',
        random: 'random port',
        ping: 'report result of ping testing port',
        same: 'in same LAN',
        optional: 'optional',
        andSome: '< - >',
        successInfo: 'Uploaded successfully'
    },
    footerInfo: {
        consult: 'QQ consult',
        bbs: 'The blue whale BBS',
        website: "The blue whale's official website",
        web: 'Blue whale zhiyun table'
    },
    otherAdd: {
        agent: 'Agent cannot be installed directly into the current business. Please contact the host manager to install agent after moving the host from the original business to the current business in CMDB',
        proxy: 'Proxy cannot be installed directly into the current business. Please contact the host manager to install agent after moving the host from the original business to the current business in CMDB',
        allStop: 'all task to the nodes in current area would be terminated!',
        someStop: 'all running tasks of other nodes related to the same task would be terminated!',
        been: 'has been in',
        blong: 'belongs to',
        size: 'business',
        business: 'installed under business',
        knowIt: 'understand',
        infoSta: 'The p-agent node exists in the current region and cannot uninstall/remove the Proxy'
    },
    addNewInfo: {
        excelInfo: 'Bulk import',
        onlyMachine: 'Import machine only',
        address: 'IP address',
        operat: 'operat',
        port: 'port',
        account: 'account',
        password: 'password',
        upload: 'Click on the upload or drag the file to here',
        reload: 'Perform the import',
        info: 'To import from EXCEL file host information. Apply to all the host password is not consistent with the scene. in the table fields from do right arrangement is as follows',
        fileError: 'File format is illegal, can only upload .XLSX file!',
        openExcel: 'Export template',
        tableName: 'Template information table',
        downloadTemplate: 'Download template of import file'
    },
    '精确': 'accurate',
    '跨页全选': 'All across the page',
    '下一步': 'Next step',
    '选择主机': 'Select host',
    '选择操作类型': 'Select operation',
    '任务详情': 'Task details',
    '不能同时对不同操作系统的主机进行操作': 'You cannot operate on hosts of different operating systems simultaneously',
    '选择操作': 'Select operation',
    '插件类型': 'Plug-in type',
    '选择插件': 'Select the plug-in',
    '选择要变更的服务': 'Select the service to change',
    '选择要更新的插件': 'Select the plug-in to update',
    '选择新包': 'Choose a new package',
    '请联系运维': 'Please contact operation staff',
    '将插件包上传到中控机的/data/src/目录并解压': 'Upload the plugin package to directory /data/src/ of the central controller and unzip it',
    '然后执行./bkeec pack gse_plugin 更新插件信息到/data/src下': 'Then execute ./bkeec pack gse_plugin to update the plug-in information under /data/src',
    '值': 'vaule',
    '文件预览': 'File preview',
    '关闭': 'close',
    '上一步': 'Previous step',
    '立即执行': 'Execute immediately',
    '进程管理': 'Process management',
    '插件更新': 'Plugin update',
    '插件': 'Plugin',
    '保留原有配置文件': 'Keep the original configuration file',
    '仅更新文件，不重启进程': 'Update files only, do not restart the process',
    '增量更新(仅覆盖)': 'Incremental update (overwrite only)',
    '覆盖更新(先删除原目录后覆盖)': 'Overwrite update (delete the original directory before overwriting)',
    '请选择插件': 'Please select plugin',
    '请选择操作': 'Please select operation',
    '请选择更新类型': 'Please select the update type',
    '请选择新包': 'Please select a new package',
    '返回列表': 'Return to the list',
    '任务类型': 'Task type',
    '目标服务': 'Target service',
    '任务ID': 'Task ID',
    '安装Proxy时，需要从Nginx所在机器下载Linux、Windows、AIX所需要的agent安装包，约150 - 180 M大小': 'Install package for OS Linux, Windows and AIX, which  sized 150 - 180 MB,  needs to be downloaded from Nginx when installing Proxy.',
    '若Proxy到Nginx之间的网络带宽较小，容易超时。可以通过增大超时时间进行设置。': "It's easy to be timeout if the network brandwidth is low. If so, higher timeout value is advised.",
    '请初始化插件信息，后台会读取中控机下的插件配置文件，如果没有初始化或者初始化失败，将无法使用插件管理相关功能': 'Please initialize the plugin information. Backend program will read the plugin configuration file. If missed or failed to do it, plugin management feature would be unusable.',
    '最后一次配置时间': 'Previous configured time',
    '到安装Agent页面查看': 'Go to the install Agent page',
    '成功': 'Success',
    '失败': 'Failed',
    '执行中': 'Executing',
    '已结束': 'Finished',
    '终止': 'Terminated',
    '操作者': 'Operator',
    '执行日志': 'Execute log',
    '当前状态': 'Current state',
    '目标机器数': 'Target machine number',
    '目标进程': 'Target process',
    '配置文件': 'Configuration file',
    '启动时间': 'Startup time',
    '云区域名称': 'Cloud area name',
    '云区域 ID': 'Cloud area ID',
    '终止成功': 'Terminated',
    '云区域': 'Cloud area',
    '时间日期': 'Time to date',
    '部署逻辑': 'Deployment of logic',
    '蓝鲸': 'Blueking',
    '受控主机': 'Host',
    '请求': 'Request',
    '从': 'From',
    '机器下载安装脚本': 'Download install scripts',
    '以及安装包': 'and packages',
    '应用从': 'from',
    '机器': 'machine',
    '登陆到目标机器': 'login target machine.',
    '等': 'and',
    '其他服务': 'Other services',
    '运行节点管理': 'Running node management',
    '所在的机器': 'machine'
}
