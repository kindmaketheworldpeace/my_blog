<template>
	<div class="bk-task" v-if="!openStatus">
        <div class="bk-task-tab" v-if="!showTabInfo">
            <div class="bk-task-search">
                <div class="bk-form-item">
                    <label class="bk-label" style="margin-right: 5px">{{$t('m["时间日期"]')}}：</label>
                    <div class="bk-form-content">
                        <bk-date-range
                            :range-separator="'--'"
                            :quick-select="true"
                            @change="changeTime">
                        </bk-date-range>
                    </div>
                </div>
                <div class="bk-form-item">
                    <label class="bk-label" style="margin-right: 5px">{{$t('m["任务类型"]')}}：</label>
                    <div class="bk-form-content">
                        <bk-selector
                            :list="taskType.list"
                            :selected.sync="taskType.selected"
                            :searchable="true"
                            @item-selected="taskTypeSelected">
                        </bk-selector>
                    </div>
                </div>
                <div class="bk-form-item">
                    <label class="bk-label" style="margin-right: 5px">{{$t('m["云区域"]')}}：</label>
                    <div class="bk-form-content">
                        <bk-selector
                            :list="cloudArea.list"
                            :selected.sync="cloudArea.selected"
                            @item-selected="cloudAreaSelected">
                        </bk-selector>
                    </div>
                </div>
                <div class="bk-task-btn">
                    <bk-button type="primary" @click="searchInfo">
                        {{$t('m.search.screen')}}
                    </bk-button>
                </div>
            </div>
            <div class="bk-tab-info" v-bkloading="{isLoading: isLoadingInfo}">
                <div class="bk-tab-head">
                    <ul>
                        <li v-for="(item, index) in tabHead" :class="{'bk-head-type': item.id === 1, 'bk-head-ip': item.id === 7}">
                            <span>{{item.name}}</span>
                        </li>
                    </ul>
                </div>
                <div class="bk-tab-body">
                    <ul>
                        <template v-if="tabList.length">
                            <li v-for="(item, index) in tabList" :class="{'bk-open-li': item.showMore}" @click="seeMoreInfo(item, index)">
                                <div class="bk-body-info bk-body-type" :class="{'bk-body-click': item.showMore}">
                                    <span class="bk-splice-icon">
                                        <i class="bk-icon icon-angle-right" v-if="!item.showMore"></i>
                                        <i class="bk-icon icon-angle-down" v-else></i>
                                    </span>
                                    <span>{{item.id}}</span>
                                </div>
                                <div class="bk-body-info" :class="{'bk-body-click': item.showMore}">{{item.job_type_desc ? item.job_type_desc : '--'}}</div>
                                <!-- <div class="bk-body-info" :class="{'bk-body-click': item.showMore}">
                                    {{item.bk_biz_id ? item.bk_biz_id : '--'}}
                                </div> -->
                                <div class="bk-body-info" :class="{'bk-body-click': item.showMore}">
                                    <span class="bk-squera">{{item.bk_cloud_id ? item.cloudAreaName : '--'}}</span>
                                </div>
                                <div class="bk-body-info" :class="{'bk-body-click': item.showMore}">
                                    <span class="bk-squera">{{item.creator ? item.creator : '--'}}</span>
                                </div>
                                <div class="bk-body-info bk-logs-parent" :class="{'bk-body-click': item.showMore}" style="position: relative;">
                                    <i class="bk-icon icon-order" :class="{'bk-mormal-color': (
                                    item.job_type.split('_')[1] === 'AGENT' || item.job_type.split('_')[1] === 'PROXY' ||
                                    item.job_type.split('_')[1] === 'PAGENT' || item.job_type === 'UPDATE_AUTHINFO'
                                    )}" @click.stop="seeLogs(item)"></i>
                                    <span class="bk-logs-info" v-if="item.job_type.split('_')[1] === 'AGENT' || item.job_type.split('_')[1] === 'PROXY' || item.job_type.split('_')[1] === 'PAGENT' || item.job_type === 'UPDATE_AUTHINFO'">
                                        {{$t('m["到安装Agent页面查看"]')}}
                                        <span class="bk-logs-icon"></span>
                                    </span>
                                </div>
                                <div class="bk-body-info bk-body-ip" :class="{'bk-body-click': item.showMore}">
                                    <span class="bk-status-success bk-status-icon" style="position: relative;">
                                        {{item.status_count ? item.status_count.success_count : '--'}}
                                        <span class="bk-status-info">{{$t('m["成功"]')}} <span class="bk-logs-icon"></span></span>
                                    </span>
                                    <span class="bk-status-error bk-status-icon" style="position: relative;">
                                        {{item.status_count ? item.status_count.failed_count : '--'}}
                                        <span class="bk-status-info">{{$t('m["失败"]')}} <span class="bk-logs-icon"></span></span>
                                    </span>
                                    <span class="bk-status-default bk-status-icon" style="position: relative;">
                                        {{item.status_count ? item.status_count.running_count : '--'}}
                                        <span class="bk-status-info">{{$t('m["执行中"]')}} <span class="bk-logs-icon"></span></span>
                                    </span>
                                </div>
                                <div class="bk-body-info" :class="{'bk-body-click': item.showMore}">
                                    <span style="color: #3c96ff; margin-right: 15px;" v-if="item.doStatus">{{$t('m["执行中"]')}}</span>
                                    <span style="color: #30d878;" v-if="!item.doStatus">{{$t('m["已结束"]')}}</span>
                                    <span 
                                        v-if="item.doStatus"
                                        class="bk-squera" 
                                        :class="{'bk-default-color': item.doStatus, 'bk-mormal-color': !item.doStatus}"
                                        @click.stop="openShade(item, index)">
                                        {{$t('m["终止"]')}}
                                    </span>
                                </div>
                                <div class="bk-more-info" v-if="item.showMore">
                                    <div class="bk-node-info" v-for="(node, index) in tabMoreInfo">
                                        <span class="bk-node-name">{{node.name}}:</span>
                                        <span class="bk-node-text">
                                            <span class="bk-squera">{{node.info ? node.info : '--'}}</span>
                                        </span>
                                    </div>
                                </div>
                            </li>
                            <li class="bk-page-size">
                                <div class="bk-table-page-top">
                                    <bk-paging
                                        :cur-page.sync="customPaging.page"
                                        :total-page="customPaging.totalPage"
                                        :type="'compact'"
                                        @page-change="pageChange">
                                    </bk-paging>
                                </div>
                            </li>
                        </template>
                        <template v-else>
                            <li v-cloak>
                                <div class="bk-result">
                                    <img src="../../images/box.png">
                                    <p>{{$t('m.tabControl.data')}}</p>
                                </div>
                            </li>
                        </template>
                    </ul>
                </div>
            </div>
        </div>
        <div class="bk-task-more" v-else>
            <task-details></task-details>
        </div>
        <!-- 二次弹窗 -->
        <div class="bk-open-shade" v-if="stopInfo.shade"></div>
            <div class="bk-open-deletedoc" v-if="stopInfo.shade">
                <div class="bk-doc-top">
                    <p>{{$t('m.message.comfireOpera')}}</p>
                </div>
                <div class="bk-doc-btn">
                    <button 
                        class="bk-button bk-primary bk-width"
                        @click="stopTask">{{$t('m.clickBtn.confirm')}}</button>
                    <button 
                        class="bk-button bk-default bk-width ml10"
                        @click="closeAll">{{$t('m.clickBtn.cancel')}}</button>
                </div>
            </div>
        </div>
	</div>
</template>

<script>
    import taskDetails from '../plug/taskDetails.vue'

    export default {
        components: {
            taskDetails
        },
        data () {
            return {
                showTabInfo: false,
                isLoadingInfo: false,
                // 任务类型
                taskType: {
                    list: [],
                    selected: 0
                },
                // 云区域信息
                cloudArea: {
                    list: [],
                    selected: 1
                },
                // 表格数据
                tabHead: [
                    {id: 1, name: this.$t('m["任务ID"]')},
                    {id: 2, name: this.$t('m["任务类型"]')},
                    // {id: 3, name: '业务'},
                    {id: 4, name: this.$t('m.tabControl.cloudArea')},
                    {id: 5, name: this.$t('m["操作者"]')},
                    {id: 6, name: this.$t('m["执行日志"]')},
                    {id: 7, name: this.$t('m["当前状态"]')},
                    {id: 8, name: this.$t('m.addNode.operation')}
                ],
                tabList: [
                    // {
                    //     id: '2018042322203359',
                    //     type: '重启 basereport',
                    //     business: '蓝鲸',
                    //     cloud: '直连区域 [5]',
                    //     operator: 'Admin',
                    //     status: '123',
                    //     logs: false,
                    //     doInfo: '终止',
                    //     doStatus: false,
                    //     showMore: false,
                    //     checkStatus: false
                    // }
                ],
                // 更多数据
                tabMoreInfo: [
                    {id: 'machinesNum', name: this.$t('m["目标机器数"]'), info: ''},
                    {id: 'process', name: this.$t('m["目标进程"]'), info: ''},
                    {id: 'configFile', name: this.$t('m["配置文件"]'), info: ''},
                    {id: 'creatTime', name: this.$t('m["启动时间"]'), info: ''},
                    {id: 'cloudName', name: this.$t('m["云区域名称"]'), info: ''},
                    {id: 'cloudId', name: this.$t('m["云区域 ID"]'), info: ''},
                    {id: 'proxy', name: 'Proxy IP', info: ''},
                    {id: 'linuxNum', name: 'Linux', info: ''},
                    {id: 'windowsNum', name: 'Windows', info: ''},
                    {id: 'aixNum', name: 'AIX', info: ''}
                ],
                moreInfo: {
                    machinesNum: '',
                    process: '',
                    configFile: '',
                    creatTime: '',
                    cloudName: '',
                    cloudId: '',
                    proxy: '',
                    linuxNum: '',
                    windowsNum: '',
                    aixNum: ''
                },
                // 分页
                customPaging: {
                    page: 1,
                    totalPage: 2,
                    pageSize: 10
                },
                // 查询信息
                queryInfo: {
                    startTime: '',
                    endTime: '',
                    jobType: '',
                    cloudArea: '0'
                },
                // 终止操作
                stopInfo: {
                    shade: false,
                    taskInfo: {}
                }
            }
        },
        computed: {
            testStore () {
                return this.$store.state.node.test
            },
            appId () {
                return this.$store.state.stall.appliId
            },
            openStatus () {
                return this.$store.state.openDoor
            }
        },
        watch: {
            appId () {
                this.clearInfo()
                this.getList()
                this.getTypeList()
            },
            openStatus () {
                this.getList()
                this.getTypeList()
            }
        },
        created () {
            if (!this.openStatus) {
                this.getList()
                this.getTypeList()
            }
        },
        methods: {
            // 清空数据
            clearInfo () {
                this.queryInfo = {
                    startTime: '',
                    endTime: '',
                    jobType: '',
                    cloudArea: '0'
                }
                this.customPaging.page = 1
            },
            // 轮询数据
            timeOutInfo () {
                let appId = this.appId
                let params = {
                    page: this.customPaging.page,
                    bk_cloud_id: this.queryInfo.cloudArea,
                    job_type: this.queryInfo.jobType,
                    start_time__gte: this.queryInfo.startTime,
                    start_time__lte: this.queryInfo.endTime
                }
                clearInterval(this.$store.state.task.timeOutInfo)
                this.$store.state.task.timeOutInfo = setInterval(() => {
                    this.$store.dispatch('task/getTaskList', {appId, params}).then((res) => {
                        for (let i = 0; i < res.data.items.length; i++) {
                            for (let j = 0; j < this.tabList.length; j++) {
                                if (res.data.items[i].id === this.tabList[j].id) {
                                    this.tabList[j].doStatus = res.data.items[i].hosts.some((item) => {
                                        return (item.status === 'RUNNING' || item.status === 'QUEUE')
                                    })
                                    this.tabList[j].status_count = res.data.items[i].status_count
                                }
                            }
                        }
                        // this.tabList = res.data.items
                        // for (let i = 0; i < this.tabList.length; i++) {
                        //     this.tabList[i].logs = false
                        //     this.tabList[i].doStatus = this.tabList[i].hosts.some((item) => {
                        //         return (item.status === 'RUNNING' || item.status === 'QUEUE')
                        //     })
                        //     this.tabList[i].showMore = false
                        //     this.tabList[i].checkStatus = false
                        // }
                        this.tabList = JSON.parse(JSON.stringify(this.tabList))
                    }, res => {
                        clearInterval(this.$store.state.task.timeOutInfo)
                        this.$bkMessage({
                            message: res.data.msg,
                            theme: 'error'
                        })
                    })
                }, 10000)
            },
            // 获取任务列表数量
            getList () {
                let info = {
                    page: 1,
                    bk_cloud_id: '0',
                    job_type: '',
                    start_time__gte: '',
                    start_time__lte: ''
                }
                this.getTaskList(info)
            },
            // ajax请求
            getTaskList (info) {
                let appId = this.appId
                let params = info
                this.isLoadingInfo = true
                this.$store.dispatch('task/getTaskList', {appId, params}).then((res) => {
                    this.customPaging.totalPage = res.data.total_page
                    this.tabList = res.data.items
                    for (let i = 0; i < this.tabList.length; i++) {
                        this.tabList[i].logs = false
                        this.tabList[i].doStatus = this.tabList[i].hosts.some((item) => {
                            return (item.status === 'RUNNING' || item.status === 'QUEUE')
                        })
                        this.tabList[i].showMore = false
                        this.tabList[i].checkStatus = false
                    }
                    this.getCloudList()
                    this.timeOutInfo()
                }, res => {
                    clearInterval(this.$store.state.task.timeOutInfo)
                    this.isLoadingInfo = false
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            // 分页
            pageChange () {
                let info = {
                    page: this.customPaging.page,
                    bk_cloud_id: this.queryInfo.cloudArea,
                    job_type: this.queryInfo.jobType,
                    start_time__gte: this.queryInfo.startTime,
                    start_time__lte: this.queryInfo.endTime
                }
                this.getTaskList(info)
                this.timeOutInfo()
            },
            // 获取任务类型数据
            getTypeList () {
                this.$store.dispatch('task/getTaskType').then((res) => {
                    this.taskType.list = []
                    this.taskType.list.push({
                        id: 'all',
                        name: this.$t('m.otherWord.all')
                    })
                    for (let i = 0; i < res.data.length; i++) {
                        this.taskType.list.push({
                            id: res.data[i].id,
                            name: res.data[i].name
                        })
                    }
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            // 获取云区域数据
            getCloudList () {
                let appId = this.appId
                if (!appId) { return }
                this.$store.dispatch('stall/getCloudInfo', {appId}).then((res) => {
                    this.cloudArea.list = []
                    this.cloudArea.list.push({
                        id: 1,
                        name: this.$t('m.tabControl.directArea'),
                        bk_cloud_id: '0'
                    })
                    for (let i = 0; i < res.data.length; i++) {
                        this.cloudArea.list.push({
                            id: i + 2,
                            name: res.data[i].bk_cloud_name,
                            bk_cloud_id: res.data[i].bk_cloud_id
                        })
                    }
                    for (let i = 0; i < this.tabList.length; i++) {
                        for (let j = 0; j < this.cloudArea.list.length; j++) {
                            if (Number(this.tabList[i].bk_cloud_id) === Number(this.cloudArea.list[j].bk_cloud_id)) {
                                this.tabList[i].cloudAreaName = this.cloudArea.list[j].name
                            }
                        }
                    }
                    this.tabList = JSON.parse(JSON.stringify(this.tabList))
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.isLoadingInfo = false
                })
            },
            // 时间日期
            changeTime (oldValue, newValue) {
                if (!newValue) {
                    this.queryInfo.startTime = ''
                    this.queryInfo.endTime = ''
                } else {
                    let val = newValue.split('--')
                    this.queryInfo.startTime = val[0].replace(/(^\s*)|(\s*$)/g, '')
                    this.queryInfo.endTime = val[1].replace(/(^\s*)|(\s*$)/g, '')
                }
                console.log(this.queryInfo.startTime, this.queryInfo.endTime)
            },
            // 任务类型
            taskTypeSelected (id, data) {
                this.queryInfo.jobType = (data.id === 'all') ? '' : data.id
            },
            // 云区域
            cloudAreaSelected (id, data) {
                this.queryInfo.cloudArea = data.bk_cloud_id
            },
            // 查询
            searchInfo () {
                this.customPaging.page = 1
                let info = {
                    page: this.customPaging.page,
                    bk_cloud_id: this.queryInfo.cloudArea,
                    job_type: this.queryInfo.jobType,
                    start_time__gte: this.queryInfo.startTime,
                    start_time__lte: this.queryInfo.endTime
                }
                this.getTaskList(info)
                this.timeOutInfo()
            },
            // 查看详情
            seeMoreInfo (item, index) {
                // for (let i = 0; i < this.tabList.length; i++) {
                //     this.tabList[i].showMore = false
                // }
                // this.tabList[index].showMore = true
                // this.tabList = JSON.parse(JSON.stringify(this.tabList))

                for (let i = 0; i < this.tabList.length; i++) {
                    if (this.tabList[i].showMore && index === i) {
                        for (let j = 0; j < this.tabList.length; j++) {
                            this.tabList[j].showMore = false
                        }
                        return
                    }
                }
                for (let i = 0; i < this.tabList.length; i++) {
                    this.tabList[i].showMore = false
                }
                this.tabList[index].showMore = true
                this.tabList = JSON.parse(JSON.stringify(this.tabList))

                this.moreInfo = {
                    machinesNum: item.host_count,
                    process: item.op_target.name,
                    configFile: item.op_target.config_file,
                    creatTime: item.start_time,
                    cloudName: item.cloudAreaName,
                    cloudId: item.bk_cloud_id,
                    proxy: '',
                    linuxNum: item.os_count.LINUX,
                    windowsNum: item.os_count.WINDOWS,
                    aixNum: item.os_count.AIX
                }
                for (let key in this.moreInfo) {
                    for (let i = 0; i < this.tabMoreInfo.length; i++) {
                        if (key === this.tabMoreInfo[i].id) {
                            this.tabMoreInfo[i].info = this.moreInfo[key]
                            break
                        }
                    }
                }
            },
            closeMoreInfo (item, index) {
                for (let i = 0; i < this.tabList.length; i++) {
                    this.tabList[i].showMore = false
                }
                this.tabList = JSON.parse(JSON.stringify(this.tabList))
            },
            // 日志
            seeLogs (item) {
                if (item.job_type.split('_')[1] === 'AGENT' ||
                  item.job_type.split('_')[1] === 'PROXY' ||
                  item.job_type === 'UPDATE_AUTHINFO' ||
                  item.job_type.split('_')[1] === 'PAGENT') { return }
                this.showTabInfo = true
                let value = item.id
                this.$store.commit('plug/changeJobId', value)
            },
            backList () {
                this.showTabInfo = false
            },
            // 终止任务
            openShade (item, index) {
                this.stopInfo.taskInfo = item
                if (!this.stopInfo.taskInfo.doStatus) { return }
                this.closeAll()
            },
            closeAll () {
                this.stopInfo.shade = !this.stopInfo.shade
            },
            stopTask () {
                let appId = this.appId
                let id = this.stopInfo.taskInfo.id
                this.$store.dispatch('stall/stopTask', {appId, id}).then((res) => {
                    this.pageChange()
                    this.$bkMessage({
                        message: this.$t('m["终止成功"]'),
                        theme: 'success'
                    })
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.closeAll()
                })
            }
        }
    }
</script>
<style lang="scss" scoped>
    @import '../../scss/mixins/clearfix.scss';
    @import '../../scss/mixins/scroller.scss';

    .bk-task {
        min-width: 1280px;
        margin: 0 auto;
        padding-top: 50px;
        padding-bottom: 100px;
    }
    .bk-task-search {
        padding: 20px 150px 20px 20px;
        position: relative;
        @include clearfix;
        background-color: #fff;
        .bk-form-item {
            float: left;
            margin-top: 0;
            /*padding-right: 20px;*/
            margin-right: 0px;
            width: 33%;
            .bk-label {
                float: left;
                line-height: 36px;
                font-size: 14px;
                color: #737987;
            }
            .bk-form-content {
                float: left;
                input {
                    height: 25px;
                }
                .bk-form-input {
                    height: 25px;
                }
            }
        }
        .bk-task-btn {
            position: absolute;
            top: 20px;
            right: 20px;
            button {
                width: 100px;
                height: 36px;
            }
        }
    }
    .bk-tab-info {
        .bk-tab-head {
            ul {
                @include clearfix;
                background-color: #fafbfd;
                border: 1px solid #dde4eb;
                li {
                    float: left;
                    font-size: 12px;
                    font-weight: bold;
                    color: #737987;
                    width: 13%;
                    line-height: 40px;
                    text-align: left;
                }
                .bk-head-type {
                    width: 18%;
                    padding-left: 72px;
                }
                .bk-head-ip {
                    width: 17%;
                }
            }
        }
        .bk-tab-body {
            ul {
                li {
                    @include clearfix;
                    border-bottom: none;
                    line-height: 43px;
                    font-size: 12px;
                    color: #737987;
                    background-color: #fff;
                    position: relative;
                    .bk-body-info {
                        float: left;
                        width: 13%;
                        text-align: left;
                        position: relative;
                        border-bottom: 1px solid #dde4eb;
                        .bk-splice-icon {
                            position: absolute;
                            top: 0;
                            left: 35px;
                            cursor: pointer;
                            .icon-angle-down {
                                color: #3e94ff;
                            }
                        }
                        .icon-order {
                            color: #3c96ff;
                            cursor: pointer;
                            font-size: 16px;
                        }
                        .bk-mormal-color {
                            color: #dde4eb;
                            cursor: not-allowed;
                        }
                        .bk-status-success,
                        .bk-status-error,
                        .bk-status-default {
                            display: inline-block;
                            width: 36px;
                            height: 18px;
                            line-height: 18px;
                            text-align: center;
                            color: #fff;
                            margin-right: 5px;
                        }
                        .bk-status-success {
                            background-color: #30d878;
                        }
                        .bk-status-error {
                            background-color: #ff5656;
                        }
                        .bk-status-default {
                            background-color: #3c96ff;
                        }
                    }
                    .bk-default-color {
                        color: #3e94ff;
                        cursor: pointer;
                    }
                    .bk-more-info {
                        position: absolute;
                        top: 44px;
                        left: 0;
                        padding: 0 170px 0 35px;
                        @include clearfix;
                        width: 100%;
                        .bk-node-info {
                            float: left;
                            width: 25%;
                        }
                        .bk-node-name {
                            width: 100px;
                            display: inline-block;
                            text-align: right;
                            font-weight: bold;
                        }
                        .bk-node-text {
                            position: relative;
                            display: inline-block;
                            margin-left: 10px;
                        }
                    }
                    .bk-logs-info {
                        position: absolute;
                        top: 8px;
                        left: 25px;
                        height: 25px;
                        color: #fff;
                        background-color: #000;
                        border-radius: 2px;
                        line-height: 25px;
                        font-size: 12px;
                        padding: 0 10px;
                        display: none;
                        .bk-logs-icon {
                            position: absolute;
                            top: 8px;
                            left: -4px;
                            width: 8px;
                            height: 8px;
                            background-color: #000;
                            transform: rotate(45deg);
                        }
                    }
                    .bk-status-icon {
                        &:hover {
                            .bk-status-info {
                                display: block;
                            }
                        }
                    }
                    .bk-status-info {
                        position: absolute;
                        top: -3px;
                        left: 44px;
                        height: 25px;
                        width: 50px;
                        color: #fff;
                        background-color: #000;
                        border-radius: 2px;
                        line-height: 25px;
                        font-size: 12px;
                        padding: 0 10px;
                        z-index: 2;
                        display: none;
                        .bk-logs-icon {
                            position: absolute;
                            top: 8px;
                            left: -4px;
                            width: 8px;
                            height: 8px;
                            background-color: #000;
                            transform: rotate(45deg);
                        }
                    }
                    .bk-logs-parent {
                        &:hover {
                            .bk-logs-info {
                                display: block;
                            }
                        }
                    }
                    .bk-body-click {
                        background-color: #ebf0f9;
                    }
                    .bk-body-type {
                        width: 18%;
                        padding-left: 72px;
                    }
                    .bk-body-ip {
                        width: 17%;
                    }
                    &.bk-open-li {
                        height: 173px;
                        border-bottom: 1px solid #dde4eb;
                    }
                }
            }
        }
    }
    /* 分页 */
    .bk-table-page-top {
        overflow: hidden;
        padding: 5px 20px;
        border-bottom: 1px solid #dde4eb;
        > span {
            display: block;
            text-align: center;
            color: #3c96ff;
            font-size: 14px;
            cursor: pointer;
            &.bk-ope-color {
                cursor: not-allowed;
            }
        }
        .bk-page {
            float: right;
        }
        .bk-page-all {
            float: left;
            margin-left: 16px;
        }
    }
    /* 暂无数据 */
    .bk-result {
        width: 100%;
        height: 580px;
        position: relative;
        border-bottom: 1px solid #dde4eb;
        > img {
            height: 50px;
            width: 100px;
            position: absolute;
            top: 40%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
        > p {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #737987;
            font-size: 18px;
        }
    }
    /* 二次弹窗 */
    .bk-open-shade {
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.5);
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
        min-width: 1180px;
        overflow: hidden;
    }
    .bk-open-deletedoc {
        width: 400px;
        box-sizing: border-box;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%,-50%);
        z-index: 1001;
        text-align: center;
        padding: 45px 65px 40px;
        background-color: #ffffff;
        border-radius: 4px;
        .bk-doc-top {
            > p {
                font-size: 24px;
                color: #212232;
                margin-bottom: 80px;
            }
        }
        .bk-doc-btn {
                .bk-width {
                width: 125px;
            }
        }
    }
</style>
