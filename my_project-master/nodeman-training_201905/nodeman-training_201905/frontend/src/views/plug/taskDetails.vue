<template>
	<div class="bk-task-details" v-bkloading="{isLoading: isLoadingInfo}">
        <div class="bk-details-title">
            <ul>
                <li v-for="(item, index) in titleList">
                    <span class="bk-title-name">{{item.name}}:</span>
                    <span class="bk-title-value">{{item.value}}</span>
                </li>
            </ul>
        </div>
        <div class="bk-details-content" ref='detailsCon'>
            <div class="bk-content-left">
                <ul>
                    <li v-for="(item, index) in lineList">
                        <div class="bk-step-name" @click="getMoreLogs(item, index)">
                            <span class="bk-step-circle" :class="item.type"></span>
                            <span class="bk-step-info" :class="item.type">{{item.display}}</span>
                        </div>
                        <div class="bk-step-line" :class="item.type" v-if="index !== lineList.length - 1"></div>
                    </li>
                </ul>
            </div>
            <div class="bk-content-right" v-bkloading="{isLoading: loadingInfo}" ref="logsMore">
                <div class="bk-content-title" :class="stepInfo.color">{{stepInfo.name ? stepInfo.name : ''}}</div>
                <div class="bk-content-logs">
                    <ul>
                        <li v-for="(item, index) in stepInfo.logsList">
                            <pre>[{{item.create_time}}] {{item.content}}</pre>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="bk-details-btn">
            <bk-button type="primary" @click="backList">
                {{$t('m["返回列表"]')}}
            </bk-button>
        </div>
	</div>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        data () {
            return {
                isLoadingInfo: false,
                loadingInfo: false,
                // 任务信息
                titleList: [
                    {id: 1, name: this.$t('m["任务类型"]'), value: ''},
                    {id: 2, name: this.$t('m["目标服务"]'), value: ''},
                    {id: 3, name: this.$t('m["任务ID"]'), value: ''}
                ],
                // 左侧任务列表
                lineList: [
                    // {
                    //     content: '上传文件到 Appo 服务器',
                    //     type: 'bk-color-success'
                    // },
                    // {
                    //     content: '分发文件到 Nginx 所在服务器',
                    //     type: 'bk-color-success'
                    // },
                    // {
                    //     content: '分发文件到中控机',
                    //     type: 'bk-color-success'
                    // },
                    // {
                    //     content: '更新文件到 gse 源包中',
                    //     type: 'bk-color-danger'
                    // },
                    // {
                    //     content: '更新所选节点上的文件 (30/250)',
                    //     type: 'bk-color-default'
                    // },
                    // {
                    //     content: '检查更新后运行状态',
                    //     type: 'bk-color-none'
                    // },
                    // {
                    //     content: '更新完成',
                    //     type: 'bk-color-none'
                    // }
                ],
                // 步骤信息
                stepInfo: {
                    name: '',
                    color: 'bk-color-default',
                    logsList: []
                },
                clickInfo: false
            }
        },
        computed: {
            appId () {
                return this.$store.state.stall.appliId
            },
            jobInfo () {
                return this.$store.state.plug.jobId
            }
        },
        created () {
            this.getAllTask()
            this.getTaskStatus()
            this.timeOutInfo()
        },
        mounted () {
            this.setCssInfo()
        },
        methods: {
            // 轮询
            timeOutInfo (item, index) {
                clearInterval(this.$store.state.plug.timeTaskInfo)
                this.$store.state.plug.timeTaskInfo = setInterval(() => {
                    let params = this.jobInfo
                    this.$store.dispatch('plug/getTask', {params}).then((res) => {
                        let valueList = res.data
                        for (let i = 0; i < this.lineList.length; i++) {
                            this.lineList[i].id = ''
                        }
                        for (let i = 0; i < this.lineList.length; i++) {
                            for (let j = 0; j < valueList.length; j++) {
                                if (this.lineList[i].display === valueList[j].content) {
                                    this.lineList[i].id = valueList[j].id
                                    if (valueList[j].status === 'SUCCESS') {
                                        this.lineList[i].type = 'bk-color-success'
                                    } else if (valueList[j].status === 'PARTIAL_SUCCESS') {
                                        this.lineList[i].type = 'bk-color-warning'
                                    } else if (valueList[j].status === 'FAILED') {
                                        this.lineList[i].type = 'bk-color-error'
                                    } else if (valueList[j].status === 'NONE') {
                                        this.lineList[i].type = 'bk-color-none'
                                    } else if (valueList[j].status === 'RUNNING') {
                                        this.lineList[i].type = 'bk-color-default'
                                    } else {
                                        this.lineList[i].type = 'bk-color-none'
                                    }
                                }
                            }
                        }
                        this.lineList = JSON.parse(JSON.stringify(this.lineList))

                        let valItem = ''
                        let valIndex = ''
                        for (let i = 0; i < this.lineList.length; i++) {
                            if (this.lineList[i].type === 'bk-color-default' || this.lineList[i].type === 'bk-color-error') {
                                valItem = this.lineList[i]
                                valIndex = i
                                break
                            }
                        }
                        if (!valItem) {
                            for (let i = this.lineList.length - 1; i >= 0; i--) {
                                if (this.lineList[i].type === 'bk-color-success') {
                                    valItem = this.lineList[i]
                                    valIndex = i
                                    break
                                }
                            }
                        }

                        let jobId = this.jobInfo
                        let stepId = this.clickInfo ? item.id : valItem.id
                        this.stepInfo.name = this.clickInfo ? item.display : valItem.display
                        this.stepInfo.color = this.clickInfo ? item.type : valItem.type
                        if (!stepId) { return }
                        this.$store.dispatch('plug/getStepLogs', {jobId, stepId}).then((res) => {
                            this.stepInfo.logsList = res.data
                        }, res => {
                            this.$bkMessage({
                                message: res.data.msg,
                                theme: 'error'
                            })
                        })
                    }, res => {
                        clearInterval(this.$store.state.plug.timeTaskInfo)
                        this.$bkMessage({
                            message: res.data.msg,
                            theme: 'error'
                        })
                    })
                }, 5000)
            },
            // 通过任务ID获取任务详情
            getTaskInfo () {
                let params = this.jobInfo
                this.isLoadingInfo = true
                this.$store.dispatch('plug/getTask', {params}).then((res) => {
                    let valueList = res.data
                    for (let i = 0; i < this.lineList.length; i++) {
                        this.lineList[i].id = ''
                    }
                    for (let i = 0; i < this.lineList.length; i++) {
                        for (let j = 0; j < valueList.length; j++) {
                            if (this.lineList[i].display === valueList[j].content) {
                                this.lineList[i].id = valueList[j].id
                                if (valueList[j].status === 'SUCCESS') {
                                    this.lineList[i].type = 'bk-color-success'
                                } else if (valueList[j].status === 'PARTIAL_SUCCESS') {
                                    this.lineList[i].type = 'bk-color-warning'
                                } else if (valueList[j].status === 'FAILED') {
                                    this.lineList[i].type = 'bk-color-error'
                                } else if (valueList[j].status === 'NONE') {
                                    this.lineList[i].type = 'bk-color-none'
                                } else if (valueList[j].status === 'RUNNING') {
                                    this.lineList[i].type = 'bk-color-default'
                                } else {
                                    this.lineList[i].type = 'bk-color-none'
                                }
                            }
                        }
                    }
                    this.lineList = JSON.parse(JSON.stringify(this.lineList))

                    // 获取分步骤日志信息
                    let valItem = ''
                    let valIndex = ''
                    for (let i = 0; i < this.lineList.length; i++) {
                        if (this.lineList[i].type === 'bk-color-default' || this.lineList[i].type === 'bk-color-error') {
                            valItem = this.lineList[i]
                            valIndex = i
                            break
                        }
                    }
                    if (!valItem) {
                        for (let i = this.lineList.length - 1; i >= 0; i--) {
                            if (this.lineList[i].type === 'bk-color-success') {
                                valItem = this.lineList[i]
                                valIndex = i
                                break
                            }
                        }
                    }
                    this.stepInfo.name = valItem.display
                    this.stepInfo.color = valItem.type
                    this.getStepLogs(valItem, valIndex)
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            // 通过ID获取所有步骤信息
            getAllTask () {
                let jobId = this.jobInfo
                let appId = this.appId
                this.$store.dispatch('plug/getAllTask', {jobId, appId}).then((res) => {
                    this.lineList = res.data
                    for (let i = 0; i < this.lineList.length; i++) {
                        this.lineList[i].type = 'bk-color-none'
                    }
                    this.getTaskInfo()
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            // 通过ID获取任务执行状态
            getTaskStatus () {
                let jobId = this.jobInfo
                let appId = this.appId
                this.$store.dispatch('plug/getTaskInfo', {jobId, appId}).then((res) => {
                    let valInfo = res.data.job_type.split('_')
                    this.titleList[0].value = res.data.job_type_desc
                    this.titleList[1].value = (valInfo[1] === 'PLUGIN') ? res.data.global_params.plugin.name : valInfo[1]
                    this.titleList[2].value = res.data.id
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            // 获取分步骤log
            getStepLogs (item, index) {
                let jobId = this.jobInfo
                let stepId = item.id
                this.loadingInfo = true
                if (!stepId) {
                    this.isLoadingInfo = false
                    this.loadingInfo = false
                    return
                }
                this.$store.dispatch('plug/getStepLogs', {jobId, stepId}).then((res) => {
                    this.stepInfo.logsList = res.data
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.isLoadingInfo = false
                    this.loadingInfo = false
                })
            },
            // 步骤选取
            getMoreLogs (item, index) {
                if (item.type === 'bk-color-none') { return }
                this.clickInfo = true
                this.stepInfo.name = item.display
                this.stepInfo.color = item.type
                this.getStepLogs(item, index)
                this.timeOutInfo(item, index)
            },
            // 返回列表
            backList () {
                clearInterval(this.$store.state.plug.timeTaskInfo)
                this.clickInfo = false
                if (this.$route.path === '/task') {
                    this.$parent.backList()
                } else if (this.$route.path === '/plug') {
                    this.$parent.originalTree()
                    this.$parent.clearTest()
                }
            },
            // 设置CSS样式高度
            setCssInfo () {
                const detailsCon = this.$refs.detailsCon
                const bodyHeight = document.body.offsetHeight
                let detailsHeight = bodyHeight - 270
                if (this.$route.path === '/plug') {
                    detailsHeight = detailsHeight - 60
                }
                detailsCon.style.cssText = 'height: ' + detailsHeight + 'px;'
            }
        }
    }
</script>
<style lang="scss" scoped>
    @import '../../scss/mixins/clearfix.scss';
    @import '../../scss/mixins/scroller.scss';

    .bk-details-title {
        height: 60px;
        line-height: 60px;
        ul {
            @include clearfix;
            position: relative;
            left: 50%;
            transform: translateX(-50%);
            width: 840px;
            li {
                float: left;
                font-size: 12px;
                color: #737987;
                padding-right: 200px;
                &:last-child {
                    padding-right: 0;
                }
                .bk-title-name {
                    font-weight: bold;
                }
            }
        }
    }
    .bk-details-content {
        width: 100%;
        /*height: 770px;*/
        min-height: 300px;
        background-color: #fff;
        padding: 36px 0px;
        border-bottom: 1px solid #dde4eb;
        @include clearfix;
        .bk-content-left {
            width: 31%;
            height: 100%;
            float: left;
            padding-left: 20%;
            @include scroller;
            overflow: auto;
            margin-right: 1%;
            ul {
                li {
                    font-size: 14px;
                    position: relative;
                    line-height: 20px;
                    padding-left: 24px;
                    color: #c3cdd7;
                    height: 60px;
                    .bk-step-circle {
                        position: absolute;
                        top: 4px;
                        left: 0;
                        border: 2px solid #c3cdd7;
                        border-radius: 50%;
                        width: 14px;
                        height: 14px;
                        cursor: pointer;
                        background-color: #fff!important;
                    }
                    .bk-step-info {
                        background-color: #fff!important;
                        cursor: pointer;
                    }
                    .bk-step-line {
                        height: 47px;
                        width: 2px;
                        background-color: #c3cdd7;
                        position: absolute;
                        left: 6px;
                        top: 17px;
                    }
                    .bk-color-default {
                        border-color: #3c96ff;
                        color: #3c96ff;
                        background-color: #3c96ff;
                    }
                    .bk-color-none {
                        border-color: #c3cdd7;
                        color: #c3cdd7;
                        background-color: #c3cdd7;
                    }
                    .bk-color-success {
                        border-color: #30d878;
                        color: #30d878;
                        background-color: #30d878;
                    }
                    .bk-color-warning {
                        border-color: #d8b843;
                        color: #d8b843;
                        background-color: #d8b843;
                    }
                    .bk-color-danger {
                        border-color: #ff5757;
                        color: #ff5757;
                        background-color: #ff5757;
                    }
                    .bk-color-error {
                        border-color: #ff5757;
                        color: #ff5757;
                        background-color: #ff5757;
                    }
                }
            }
        }
        .bk-content-right {
            width: 67%;
            height: 100%;
            float: left;
            overflow: auto;
            @include scroller;
            padding-left: 22px;
            border-left: 1px solid #dde4eb;
            .bk-content-title {
                font-size: 16px;
                margin-bottom: 16px;
            }
            .bk-content-logs {
                @include scroller;
                overflow: auto;
                li {
                    line-height: 24px;
                    font-size: 12px;
                    color: #737987;
                }
            }
            .bk-color-default {
                color: #3c96ff;
            }
            .bk-color-none {
                color: #c3cdd7;
            }
            .bk-color-success {
                color: #30d878;
            }
            .bk-color-danger {
                color: #ff5757;
            }
            .bk-color-warning {
                color: #d8b843;
            }
            .bk-color-error {
                color: #ff5757;
            }
        }
    }
    .bk-details-btn {
        text-align: center;
        margin-top: 20px;
        button {
            width: 100px;
            height: 36px;
            line-height: 36px;
        }
    }
</style>
