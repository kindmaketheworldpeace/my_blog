<template>
	<div class="bk-plug" v-if="!openStatus">
        <div class="bk-plug-step">
            <ul>
                <li v-for="(item, index) in stepInfo" :class="{'bk-step-complete': item.complete}">
                    <div class="bk-step-num" :class="{'bk-complete-border': item.complete}">{{item.id}}</div>
                    <div class="bk-step-info" :class="{'bk-step-complete': item.complete}">{{item.name}}</div>
                    <div class="bk-step-interval" :class="{'bk-step-complete': item.complete}" v-if="index !== stepInfo.length-1">.......</div>
                </li>
            </ul>
        </div>
        <!-- 第一步 -->
        <div class="bk-plug-first" v-if="treeStatus.hostShow" style="padding-top: 60px;">
            <div class="bk-plug-search">
                <div class="bk-form-item">
                    <label class="bk-label" style="margin-right: 5px">SET：</label>
                    <div class="bk-form-content">
                        <bk-selector
                            :list="selectInfo.setList"
                            :selected.sync="selectInfo.setSelected"
                            @item-selected="selectSet">
                        </bk-selector>
                    </div>
                </div>
                <div class="bk-form-item">
                    <label class="bk-label" style="margin-right: 5px">{{$t('m.search.modules')}}：</label>
                    <div class="bk-form-content">
                        <bk-selector
                            :list="selectInfo.module"
                            :selected.sync="selectInfo.moduleSelected"
                            :disabled="selectInfo.setSelected === 0"
                            @item-selected="selectModule">
                        </bk-selector>
                    </div>
                </div>
                <div class="bk-form-item">
                    <label class="bk-label" style="margin-right: 5px">{{$t('m.tabControl.cloudArea')}}：</label>
                    <div class="bk-form-content">
                        <bk-selector
                            :list="selectInfo.cloudArea"
                            :selected.sync="selectInfo.cloudSelected"
                            @item-selected="selectCloud">
                        </bk-selector>
                    </div>
                </div>
                <!-- <div class="bk-form-item">
                    <label class="bk-label" style="margin-right: 5px">操作系统：</label>
                    <div class="bk-form-content">
                        <bk-selector
                            :list="selectInfo.system"
                            :selected.sync="selectInfo.systemSelected"
                            @item-selected="selectSystem">
                        </bk-selector>
                    </div>
                </div> -->
                <div class="bk-form-item">
                    <label class="bk-label" style="margin-right: 5px">{{$t('m["精确"]')}} IP：</label>
                    <div class="bk-form-content ip-wrapper">
                        <!-- <input type="text" class="bk-form-input" v-model="searchInfo.ipInfo"> -->
                        <textarea class="bk-form-textarea" v-model="searchInfo.ipInfo" @focus="changTextarea"></textarea>
                    </div>
                </div>
                <div class="bk-form-btn">
                    <bk-button type="primary" title="$t('m.clickBtn.confirm')" @click="submitSelect">
                        {{$t('m.clickBtn.confirm')}}
                    </bk-button>
                </div>
            </div>
            <div class="bk-tab-info" v-bkloading="{isLoading: isLoadingInfo}">
                <div class="bk-tab-head">
                    <ul>
                        <li v-for="(item, index) in tabHead"
                            class="bk-cursor"
                            :class="{'bk-head-type': item.id === 1, 'bk-head-ip': item.id === 2}"
                            @click="showMoreSearch(item, index)">
                            <label class="bk-form-checkbox bk-checkbox-small" v-if="item.id === 1">
                                <input type="checkbox" name="checkbox1" :checked="allCheck" @click="checkAll">
                            </label>
                            <span :class="{'bk-cursor': index !== 0 && index !== 1, 'bk-blue-color': showColor === index}"
                                class="bk-tab-parent">{{item.name}}</span>
                            <span v-if="index !== 0 && index !== 1"
                                :class="{'bk-blue-color': showColor === index}"
                                class="bk-tab-icon bk-cursor bk-tab-parent">
                                <i class="bk-icon icon-funnelConfig"></i>
                            </span>
                            <transition name="moreInfo">
                                <div class="bk-select-more" v-if="showSelect === item.id">
                                    <ul>
                                        <li v-for="(node, index) in searchList"
                                            :class="{'bk-click-info': node.id === selectId}"
                                            @click="changeConditions(node, index)">
                                            {{node.name}}
                                        </li>
                                    </ul>
                                </div>
                            </transition>
                        </li>
                    </ul>
                </div>
                <div class="bk-tab-body">
                    <ul>
                        <template v-if="tabList.length">
                            <li v-for="(item, index) in tabList" :class="{'bk-open-li': item.showMore}"@click="seeMoreInfo(item, index)">
                                <div class="bk-body-info bk-body-type" :class="{'bk-body-click': item.showMore}">
                                    <label class="bk-form-checkbox bk-checkbox-small">
                                        <div class="bk-spin-loading bk-spin-loading-mini bk-spin-loading-primary" v-if="item.disInfo">
                                            <div class="rotate rotate1"></div>
                                            <div class="rotate rotate2"></div>
                                            <div class="rotate rotate3"></div>
                                            <div class="rotate rotate4"></div>
                                            <div class="rotate rotate5"></div>
                                            <div class="rotate rotate6"></div>
                                            <div class="rotate rotate7"></div>
                                            <div class="rotate rotate8"></div>
                                        </div>
                                        <input
                                            v-else
                                            type="checkbox"
                                            name="checkbox1"
                                            :checked="item.checkStatus"
                                            @click.stop="checkOneStatus(item, index)"
                                            :disabled="item.stateInfomation.agentSta !== 'success'">
                                    </label>
                                    <span class="bk-splice-icon">
                                        <i
                                            class="bk-icon icon-angle-right"
                                            v-if="!item.showMore">
                                        </i>
                                        <i
                                            class="bk-icon icon-angle-down"
                                            v-else >
                                        </i>
                                    </span>
                                    <span
                                        :class="{'bk-none-agent': item.stateInfomation.agentVersion === '--'}">{{item.node_type === 'AGENT' ? 'Agent' : (item.node_type === 'PAGENT' ? 'P-Agent' : 'Proxy')}}
                                    </span>
                                </div>
                                <div
                                    class="bk-body-info bk-body-ip"
                                    :class="{'bk-body-click': item.showMore,
                                    'bk-none-agent': item.stateInfomation.agentVersion === '--'}">
                                    <span :class="{'bk-ip-info': (!!item.login_ip)}">{{item.conn_ip}}</span>
                                    <span :class="{'bk-ip-info': (!!item.login_ip)}">{{item.login_ip}}</span>
                                </div>
                                <div
                                    class="bk-body-info"
                                    :class="{'bk-body-click': item.showMore,
                                    'bk-none-agent': item.stateInfomation.agentVersion === '--'}">
                                    {{item.os_type}}
                                </div>
                                <div class="bk-body-info" :class="{'bk-body-click': item.showMore}">
                                    <span
                                        class="bk-node-squear"
                                        :class="{
                                        'bk-squera-normal': item.stateInfomation.agentSta === 'normal',
                                        'bk-squera-error': item.stateInfomation.agentSta === 'error'}"></span>
                                    <span class="bk-squera"
                                        :class="{'bk-none-agent': item.stateInfomation.agentVersion === '--'}">{{item.stateInfomation.agentVersion || '--'}}
                                    </span>
                                </div>
                                <div class="bk-body-info" :class="{'bk-body-click': item.showMore}">
                                    <span class="bk-node-squear" :class="{
                                    'bk-squera-normal': item.stateInfomation.basereportSta === 'normal',
                                    'bk-squera-error': item.stateInfomation.basereportSta === 'error'}"></span>
                                    <span class="bk-squera"
                                        :class="{'bk-none-agent': item.stateInfomation.agentVersion === '--'}">{{item.stateInfomation.basereportVersion || '--'}}
                                    </span>
                                </div>
                                <div class="bk-body-info" :class="{'bk-body-click': item.showMore}">
                                    <span class="bk-node-squear" :class="{
                                    'bk-squera-normal': item.stateInfomation.unifytlogcSta === 'normal',
                                    'bk-squera-error': item.stateInfomation.unifytlogcSta === 'error'}"></span>
                                    <span class="bk-squera"
                                        :class="{'bk-none-agent': item.stateInfomation.agentVersion === '--'}">{{item.stateInfomation.unifytlogcVersion || '--'}}</span>
                                </div>
                                <div class="bk-body-info" :class="{'bk-body-click': item.showMore}">
                                    <span class="bk-node-squear" :class="{
                                    'bk-squera-normal': item.stateInfomation.processbeatSta === 'normal',
                                    'bk-squera-error': item.stateInfomation.processbeatSta === 'error'}"></span>
                                    <span class="bk-squera"
                                        :class="{'bk-none-agent': item.stateInfomation.agentVersion === '--'}">{{item.stateInfomation.processbeatVersion || '--'}}</span>
                                </div>
                                <div class="bk-body-info" :class="{'bk-body-click': item.showMore}" style="padding-right: 50px">
                                    <span class="bk-node-squear" :class="{
                                    'bk-squera-normal': item.stateInfomation.bkmetricSta === 'normal',
                                    'bk-squera-error': item.stateInfomation.bkmetricSta === 'error'}"></span>
                                    <span class="bk-squera"
                                        :class="{'bk-none-agent': item.stateInfomation.agentVersion === '--'}">{{item.stateInfomation.bkmetricVersion || '--'}}</span>
                                    <!-- 查看日志 -->
                                    <img
                                        class="bk-image-order"
                                        v-if="item.disInfo"
                                        src="../../images/word.png"
                                        @click.stop="showSlider(item, index)">
                                </div>
                                <div class="bk-more-info" v-if="item.showMore">
                                    <div class="bk-node-info" v-for="(node, index) in item.status">
                                        <span class="bk-node-name">{{node.name === 'gseagent' ? 'agent' : node.name}}：</span>
                                        <span class="bk-node-text">
                                            <span class="bk-node-squear" :class="{
                                            'bk-squera-normal': (node.status === 'UNKNOWN' || node.status === 'UNREGISTER'),
                                            'bk-squera-error': node.status === 'TERMINATED'}"></span>
                                            <span class="bk-squera"
                                                style="margin-left: 28px;"
                                                :class="{'bk-none-agent': item.stateInfomation.agentVersion === '--'}">{{node.version ? node.version : '--'}}</span>
                                        </span>
                                    </div>
                                </div>
                            </li>
                            <li class="bk-page-size">
                                <div class="bk-table-page-top">
                                    <bk-paging
                                        style="margin-top: 4px;"
                                        :cur-page.sync="customPaging.page"
                                        :total-page="customPaging.totalPage"
                                        :type="'compact'"
                                        @page-change="pageChange">
                                    </bk-paging>
                                    <div class="bk-page-all">
                                        <label class="bk-form-checkbox bk-checkbox-small">
                                            <input type="checkbox" name="checkbox1" :checked="pageAllCheck" @click="getAllTabList">
                                        </label>
                                        <span>{{$t('m["跨页全选"]')}}</span>
                                    </div>
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
            <div class="bk-plug-button">
                <bk-button type="primary"
                    @click="nextStep"
                    :disabled="!checkList.length">
                    {{$t('m["下一步"]')}}
                </bk-button>
            </div>
        </div>
        <!-- 第二步 -->
        <div class="bk-plug-second" v-if="treeStatus.typeShow" style="padding-top: 60px;">
            <operation :ip-info="ipInfo"></operation>
        </div>
        <!-- 第三步 -->
        <div class="bk-plug-third" v-if="treeStatus.taskShow" style="padding-top: 60px;">
            <task-details></task-details>
        </div>
        <!-- 日志弹框 -->
        <bk-sideslider :is-show.sync="cmdbSettings.isShow" :title="cmdbSettings.title" :width="553" :quick-close="true">
            <div class="p20 bk-open-window" slot="content">
                <!-- 详细安装步骤 -->
                <div class="bk-install-step" id="bkStep">
                    <div class="bk-step-info" v-html="cmdbSettings.info"></div>
                </div>
            </div>
        </bk-sideslider>
	</div>
</template>

<script>
    import operation from './operation.vue'
    import taskDetails from './taskDetails.vue'

    export default {
        components: {
            operation,
            taskDetails
        },
        data () {
            return {
                isLoadingInfo: false,
                // 数状态
                treeStatus: {
                    hostShow: true,
                    typeShow: false,
                    taskShow: false
                },
                // 步骤信息
                stepInfo: [
                    {id: 1, name: this.$t('m["选择主机"]'), complete: true},
                    {id: 2, name: this.$t('m["选择操作类型"]'), complete: false},
                    {id: 3, name: this.$t('m["任务详情"]'), complete: false}
                ],
                // 搜索信息
                selectInfo: {
                    setList: [],
                    setAllList: [],
                    setSelected: 0,
                    module: [],
                    moduleSelected: 0,
                    cloudArea: [],
                    cloudSelected: 1,
                    system: [],
                    systemSelected: 0
                },
                searchInfo: {
                    setInfo: '',
                    moduleInfo: '',
                    cloudInfo: '0',
                    systemInfo: '',
                    ipInfo: ''
                },
                // 表格搜索功能
                searchList: [],
                selectId: 1,
                showSelect: -1,
                showColor: -1,
                tabHeadInfo: {
                    status__name: '',
                    status__proc_type: '',
                    status__version: ''
                },
                // 表格信息
                tabHead: [
                    {id: 1, name: this.$t('m.addNode.nodeType')},
                    {id: 2, name: this.$t('m.addNode.address')},
                    {id: 3, name: this.$t('m.addNode.operat')},
                    {id: 4, name: 'gseagent'},
                    {id: 5, name: 'basereport'},
                    {id: 6, name: 'unifytlogc'},
                    {id: 7, name: 'processbeat'},
                    {id: 8, name: 'bkmetricbeat'}
                ],
                tabList: [
                    // {
                    //     type: 'Agent',
                    //     ip: '10.124.10.144',
                    //     system: 'Linux',
                    //     agent: '1.3.45(正常)',
                    //     basereport: '1.3.45(正常)',
                    //     unifytlogc: '1.3.45(正常)',
                    //     processbeat: '1.3.45(正常)',
                    //     bkmetric: '1.3.45(正常)',
                    //     showMore: false,
                    //     checkStatus: false,
                    //     state: {
                    //         agentSta: 'success',
                    //         basereportSta: 'success',
                    //         unifytlogcSta: 'normal',
                    //         processbeatSta: 'success',
                    //         bkmetricSta: 'error'
                    //     }
                    // },
                    // {
                    //     type: 'Agent',
                    //     ip: '10.124.10.144',
                    //     system: 'Linux',
                    //     agent: '1.3.45(正常)',
                    //     basereport: '1.3.45(正常)',
                    //     unifytlogc: '1.3.45(正常)',
                    //     processbeat: '1.3.45(正常)',
                    //     bkmetric: '1.3.45(正常)',
                    //     showMore: false,
                    //     checkStatus: false,
                    //     state: {
                    //         agentSta: 'success',
                    //         basereportSta: 'success',
                    //         unifytlogcSta: 'normal',
                    //         processbeatSta: 'success',
                    //         bkmetricSta: 'error'
                    //     }
                    // }
                ],
                allCheck: false,
                pageAllCheck: false,
                checkList: [],
                allTabList: [],
                // 分页
                customPaging: {
                    page: 1,
                    totalPage: 2,
                    pageSize: 10
                },
                // 向子组件传的值
                ipInfo: {
                    bk_cloud_id: '2',
                    hosts: []
                },
                // 节点日志信息
                cmdbSettings: {
                    isShow: false,
                    title: this.$t('m.openSlider.stepInfo'),
                    info: '123'
                },
                stepInterval: '',
                logId: ''
            }
        },
        computed: {
            appId () {
                return this.$store.state.stall.appliId
            },
            testStore () {
                return this.$store.state.node.test
            },
            openStatus () {
                return this.$store.state.openDoor
            }
        },
        watch: {
            appId () {
                this.clearInfo()
                this.getSearchInfo()
                this.getOperatType()
            },
            openStatus () {
                this.getTabList()
                this.getSearchInfo()
                this.getOperatType()
            }
        },
        created () {
            if (!this.openStatus) {
                this.getTabList()
                this.getSearchInfo()
                this.getOperatType()
            }
        },
        methods: {
            changTextarea () {
                this.searchInfo.ipInfo = this.searchInfo.ipInfo.replace(',', '\n')
            },
            // 清空数据
            clearInfo () {
                this.checkList = []
                this.pageAllCheck = false
                this.allCheck = false
                this.customPaging.page = 1
                this.searchInfo = {
                    setInfo: '',
                    moduleInfo: '',
                    cloudInfo: '0',
                    systemInfo: '',
                    ipInfo: ''
                }
                this.getTabList()
            },
            clearTest () {
                this.checkList = []
                this.pageAllCheck = false
                this.allCheck = false
                this.submitSelect()
            },
            // 轮询数据
            timeOutInfo () {
                if (!this.appId) { return }
                this.searchInfo.ipInfo = this.searchInfo.ipInfo.replace(/\n/g, ',').trim()
                this.searchInfo.ipInfo = this.searchInfo.ipInfo.indexOf(',', this.searchInfo.ipInfo.length - 1) !== -1 ? this.searchInfo.ipInfo.substring(0, this.searchInfo.ipInfo.lastIndexOf(',')) : this.searchInfo.ipInfo
                let params = {
                    bk_cloud_id: this.searchInfo.cloudInfo,
                    bk_set_id: this.searchInfo.setInfo,
                    bk_module_id: this.searchInfo.moduleInfo,
                    os_type: this.searchInfo.systemInfo,
                    ip: this.searchInfo.ipInfo,
                    page: this.customPaging.page,
                    object_type: 'all',
                    status__name: this.tabHeadInfo.status__name,
                    status__proc_type: this.tabHeadInfo.status__proc_type,
                    status__version: this.tabHeadInfo.status__version
                }
                let appId = this.appId
                clearInterval(this.$store.state.plug.timeInfo)
                this.$store.state.plug.timeInfo = setInterval(() => {
                    this.$store.dispatch('plug/getTabList', {params, appId}).then((res) => {
                        let valList = res.data.items
                        for (let i = 0; i < valList.length; i++) {
                            for (let j = 0; j < this.tabList.length; j++) {
                                if (valList[i].id === this.tabList[j].id) {
                                    this.tabList[j].disInfo = (valList[i].job_result.status === 'QUEUE' || valList[i].job_result.status === 'RUNNING')
                                    for (let t = 0; t < valList[i].status.length; t++) {
                                        let valStatus = valList[i].status[t]
                                        if (valStatus.name === 'gseagent') {
                                            this.filterPackgeInfo(valStatus, this.tabList[i].stateInfomation, 'agentVersion', 'agentSta')
                                        }
                                        if (valStatus.name === 'basereport') {
                                            this.filterPackgeInfo(valStatus, this.tabList[i].stateInfomation, 'basereportVersion', 'basereportSta')
                                        }
                                        if (valStatus.name === 'unifytlogc') {
                                            this.filterPackgeInfo(valStatus, this.tabList[i].stateInfomation, 'unifytlogcVersion', 'unifytlogcSta')
                                        }
                                        if (valStatus.name === 'processbeat') {
                                            this.filterPackgeInfo(valStatus, this.tabList[i].stateInfomation, 'processbeatVersion', 'processbeatSta')
                                        }
                                        if (valStatus.name === 'bkmetricbeat') {
                                            this.filterPackgeInfo(valStatus, this.tabList[i].stateInfomation, 'bkmetricVersion', 'bkmetricSta')
                                        }
                                    }
                                }
                            }
                        }
                        this.tabList = JSON.parse(JSON.stringify(this.tabList))
                    }, res => {
                        clearInterval(this.$store.state.plug.timeInfo)
                        this.$bkMessage({
                            message: res.data.msg,
                            theme: 'error'
                        })
                    })
                }, 10000)
            },
            // 跨页全选
            getAllTabList () {
                this.pageAllCheck = !this.pageAllCheck
                this.allCheck = this.pageAllCheck
                for (let i = 0; i < this.tabList.length; i++) {
                    this.tabList[i].checkStatus = this.pageAllCheck
                    if (this.tabList[i].disInfo || this.tabList[i].stateInfomation.agentVersion === '--') {
                        this.tabList[i].checkStatus = false
                    }
                }
                this.tabList = JSON.parse(JSON.stringify(this.tabList))
                if (!this.pageAllCheck) {
                    this.allTabList = []
                    this.checkList = []
                } else {
                    this.searchInfo.ipInfo = this.searchInfo.ipInfo.replace(/\n/g, ',').trim()
                    this.searchInfo.ipInfo = this.searchInfo.ipInfo.indexOf(',', this.searchInfo.ipInfo.length - 1) !== -1 ? this.searchInfo.ipInfo.substring(0, this.searchInfo.ipInfo.lastIndexOf(',')) : this.searchInfo.ipInfo
                    let params = {
                        bk_cloud_id: this.searchInfo.cloudInfo,
                        bk_set_id: this.searchInfo.setInfo,
                        bk_module_id: this.searchInfo.moduleInfo,
                        os_type: this.searchInfo.systemInfo,
                        ip: this.searchInfo.ipInfo,
                        page: this.customPaging.page,
                        ignore_page: '1',
                        object_type: 'all',
                        status__name: this.tabHeadInfo.status__name,
                        status__proc_type: this.tabHeadInfo.status__proc_type,
                        status__version: this.tabHeadInfo.status__version
                    }
                    let appId = this.appId
                    this.$store.dispatch('plug/getTabList', {params, appId}).then((res) => {
                        this.allTabList = res.data
                        for (let i = 0; i < this.allTabList.length; i++) {
                            this.allTabList[i].showMore = false
                            this.allTabList[i].checkStatus = true
                            this.allTabList[i].stateInfomation = {
                                agentSta: 'normal',
                                agentVersion: '',
                                basereportSta: 'normal',
                                basereportVersion: '',
                                unifytlogcSta: 'normal',
                                unifytlogcVersion: '',
                                processbeatSta: 'normal',
                                processbeatVersion: '',
                                bkmetricSta: 'normal',
                                bkmetricVersion: ''
                            }
                            for (let j = 0; j < this.allTabList[i].status.length; j++) {
                                let valStatus = this.allTabList[i].status[j]
                                if (valStatus.name === 'gseagent') {
                                    this.filterPackgeInfo(valStatus, this.allTabList[i].stateInfomation, 'agentVersion', 'agentSta')
                                }
                            }
                        }
                        this.checkList = this.allTabList
                        for (let i = this.checkList.length - 1; i >= 0; i--) {
                            if (this.checkList[i].job_result.status === 'QUEUE' || this.checkList[i].job_result.status === 'RUNNING' || this.checkList[i].stateInfomation.agentSta !== 'success') {
                                this.checkList.splice(i, 1)
                            }
                        }
                    }, res => {
                        this.$bkMessage({
                            message: res.data.msg,
                            theme: 'error'
                        })
                    })
                }
            },
            // 初始化表格数据
            getTabList () {
                let params = {
                    bk_cloud_id: '0',
                    bk_set_id: '',
                    bk_module_id: '',
                    os_type: '',
                    object_type: 'all'
                }
                this.getTabAjax(params)
            },
            // 请求方法体
            getTabAjax (value) {
                if (!this.appId) { return }
                let params = value
                let appId = this.appId
                this.isLoadingInfo = true
                this.$store.dispatch('plug/getTabList', {params, appId}).then((res) => {
                    this.tabList = res.data.items
                    for (let i = 0; i < this.tabList.length; i++) {
                        this.tabList[i].showMore = false
                        this.tabList[i].checkStatus = false
                        this.tabList[i].disInfo = false
                        this.tabList[i].stateInfomation = {
                            agentSta: 'normal',
                            agentVersion: '',
                            basereportSta: 'normal',
                            basereportVersion: '',
                            unifytlogcSta: 'normal',
                            unifytlogcVersion: '',
                            processbeatSta: 'normal',
                            processbeatVersion: '',
                            bkmetricSta: 'normal',
                            bkmetricVersion: ''
                        }
                        if (this.tabList[i].job_result.status === 'QUEUE' || this.tabList[i].job_result.status === 'RUNNING') {
                            this.tabList[i].disInfo = true
                        }
                        for (let j = 0; j < this.tabList[i].status.length; j++) {
                            let valStatus = this.tabList[i].status[j]
                            if (valStatus.name === 'gseagent') {
                                this.filterPackgeInfo(valStatus, this.tabList[i].stateInfomation, 'agentVersion', 'agentSta')
                            }
                            if (valStatus.name === 'basereport') {
                                this.filterPackgeInfo(valStatus, this.tabList[i].stateInfomation, 'basereportVersion', 'basereportSta')
                            }
                            if (valStatus.name === 'unifytlogc') {
                                this.filterPackgeInfo(valStatus, this.tabList[i].stateInfomation, 'unifytlogcVersion', 'unifytlogcSta')
                            }
                            if (valStatus.name === 'processbeat') {
                                this.filterPackgeInfo(valStatus, this.tabList[i].stateInfomation, 'processbeatVersion', 'processbeatSta')
                            }
                            if (valStatus.name === 'bkmetricbeat') {
                                this.filterPackgeInfo(valStatus, this.tabList[i].stateInfomation, 'bkmetricVersion', 'bkmetricSta')
                            }
                        }
                    }
                    this.customPaging.totalPage = res.data.total_page
                    this.tabList = JSON.parse(JSON.stringify(this.tabList))
                    // 跨页选中
                    for (let i = 0; i < this.checkList.length; i++) {
                        for (let j = 0; j < this.tabList.length; j++) {
                            if (this.checkList[i].id === this.tabList[j].id) {
                                this.tabList[j].checkStatus = true
                            }
                        }
                    }
                    this.timeOutInfo()
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.isLoadingInfo = false
                })
            },
            filterPackgeInfo (item, tabItem, versionInfo, staInfo) {
                tabItem[versionInfo] = item.version
                if (item.status === 'RUNNING') {
                    tabItem[staInfo] = 'success'
                }
                if (item.status === 'TERMINATED') {
                    tabItem[staInfo] = 'error'
                }
                if (item.status === 'UNKNOWN' || item.status === 'UNREGISTER') {
                    tabItem[staInfo] = 'normal'
                }
            },
            // 分页
            pageChange () {
                this.allCheck = this.pageAllCheck
                for (let i = 0; i < this.tabList.length; i++) {
                    if (!this.tabList[i].checkStatus) {
                        this.allCheck = false
                        break
                    }
                }
                this.searchInfo.ipInfo = this.searchInfo.ipInfo.replace(/\n/g, ',').trim()
                this.searchInfo.ipInfo = this.searchInfo.ipInfo.indexOf(',', this.searchInfo.ipInfo.length - 1) !== -1 ? this.searchInfo.ipInfo.substring(0, this.searchInfo.ipInfo.lastIndexOf(',')) : this.searchInfo.ipInfo
                let params = {
                    bk_cloud_id: this.searchInfo.cloudInfo,
                    bk_set_id: this.searchInfo.setInfo,
                    bk_module_id: this.searchInfo.moduleInfo,
                    os_type: this.searchInfo.systemInfo,
                    ip: this.searchInfo.ipInfo,
                    page: this.customPaging.page,
                    object_type: 'all',
                    status__name: this.tabHeadInfo.status__name,
                    status__proc_type: this.tabHeadInfo.status__proc_type,
                    status__version: this.tabHeadInfo.status__version
                }
                this.getTabAjax(params)
                this.timeOutInfo()
            },
            // 查询数据
            submitSelect () {
                this.checkList = []
                this.allCheck = false
                this.customPaging.page = 1
                this.searchInfo.ipInfo = this.searchInfo.ipInfo.replace(/\n/g, ',').trim()
                this.searchInfo.ipInfo = this.searchInfo.ipInfo.indexOf(',', this.searchInfo.ipInfo.length - 1) !== -1 ? this.searchInfo.ipInfo.substring(0, this.searchInfo.ipInfo.lastIndexOf(',')) : this.searchInfo.ipInfo
                let params = {
                    bk_cloud_id: this.searchInfo.cloudInfo,
                    bk_set_id: this.searchInfo.setInfo,
                    bk_module_id: this.searchInfo.moduleInfo,
                    os_type: this.searchInfo.systemInfo,
                    ip: this.searchInfo.ipInfo,
                    page: this.customPaging.page,
                    object_type: 'all',
                    status__name: this.tabHeadInfo.status__name,
                    status__proc_type: this.tabHeadInfo.status__proc_type,
                    status__version: this.tabHeadInfo.status__version
                }
                this.getTabAjax(params)
                this.timeOutInfo()
            },
            // 显示表头的下拉查询数据
            showMoreSearch (item, index) {
                if (index === 0 || index === 1) { return }
                this.selectId = this.showColor === index ? this.selectId : 1
                this.showColor = index
                this.changeSearchInfo(item)
                if (index !== 2) {
                    this.tabHeadInfo.status__name = item.name
                    this.tabHeadInfo.status__proc_type = item.name === 'gseagent' ? 'agent' : 'plugin'
                }
            },
            changeSearchInfo (item) {
                if (item.name === this.$t('m.addNode.operat')) {
                    this.searchList = this.selectInfo.system
                    this.showSelect = this.showSelect === item.id ? -1 : item.id
                    return
                }
                let obj = {
                    agent: 'gseagent',
                    basereport: 'basereport',
                    unifytlogc: 'unifytlogc',
                    processbeat: 'processbeat',
                    bkmetricbeat: 'bkmetricbeat'
                }
                for (let key in obj) {
                    if (item.name === obj[key]) {
                        let appId = this.appId
                        let params = {
                            proc_type: item.name === 'gseagent' ? 'agent' : 'plugin',
                            name: item.name
                        }
                        this.$store.dispatch('plug/getVersion', {appId, params}).then((res) => {
                            this.searchList = []
                            this.searchList.push({
                                id: 1,
                                name: this.$t('m.otherWord.all')
                            })
                            for (let i = 0; i < res.data.length; i++) {
                                if (res.data[i].version) {
                                    this.searchList.push({
                                        id: i + 2,
                                        name: res.data[i].version
                                    })
                                }
                            }
                        }, res => {
                            this.searchList = []
                            this.searchList.push({
                                id: 1,
                                name: this.$t('m.otherWord.all')
                            })
                            this.$bkMessage({
                                message: res.data.msg,
                                theme: 'error'
                            })
                        }).finally(() => {
                            this.showSelect = this.showSelect === item.id ? -1 : item.id
                        })
                    }
                }
            },
            // 选择一个查询结果
            changeConditions (node, index) {
                this.selectId = node.id
                if (this.showColor === 2) {
                    this.tabHeadInfo = {
                        status__name: '',
                        status__proc_type: '',
                        status__version: ''
                    }
                    this.searchInfo.systemInfo = node.name === this.$t('m.otherWord.all') ? '' : node.name
                } else {
                    this.tabHeadInfo.status__version = node.name === this.$t('m.otherWord.all') ? '' : node.name
                    this.searchInfo.systemInfo = ''
                }
                this.searchInfo.ipInfo = this.searchInfo.ipInfo.replace(/\n/g, ',').trim()
                this.searchInfo.ipInfo = this.searchInfo.ipInfo.indexOf(',', this.searchInfo.ipInfo.length - 1) !== -1 ? this.searchInfo.ipInfo.substring(0, this.searchInfo.ipInfo.lastIndexOf(',')) : this.searchInfo.ipInfo
                let params = {
                    bk_cloud_id: this.searchInfo.cloudInfo,
                    bk_set_id: this.searchInfo.setInfo,
                    bk_module_id: this.searchInfo.moduleInfo,
                    ip: this.searchInfo.ipInfo,
                    page: this.customPaging.page,
                    object_type: 'all',
                    os_type: this.searchInfo.systemInfo,
                    status__name: this.tabHeadInfo.status__name,
                    status__proc_type: this.tabHeadInfo.status__proc_type,
                    status__version: this.tabHeadInfo.status__version
                }
                this.getTabAjax(params)
            },
            // 获取查询列表数据
            getSearchInfo () {
                this.getSetList()
                this.getCloudList()
            },
            getSetList () {
                // 获取SET列表数据
                let appId = this.appId
                if (!appId) { return }
                this.selectInfo.setList = []
                this.$store.dispatch('stall/getCmdbInfo', {appId}).then((res) => {
                    this.selectInfo.setAllList = res.data
                    this.selectInfo.setList.push({
                        id: 1,
                        name: this.$t('m.otherWord.all'),
                        bk_set_id: ''
                    })
                    for (let i = 0; i < this.selectInfo.setAllList.length; i++) {
                        this.selectInfo.setList.push({
                            id: i + 2,
                            name: this.selectInfo.setAllList[i].SetName,
                            bk_set_id: this.selectInfo.setAllList[i].SetID
                        })
                    }
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            getModuleList (data) {
                // 获取模块列表数据
                let temp = 0
                if (data.bk_set_id === '') {
                    this.selectInfo.module.push({
                        id: 1,
                        name: this.$t('m.otherWord.all'),
                        bk_module_id: ''
                    })
                    for (let i = 0; i < this.selectInfo.setAllList.length; i++) {
                        temp += this.selectInfo.setAllList[i].Children.length
                        for (let j = 0; j < this.selectInfo.setAllList[i].Children.length; j++) {
                            this.selectInfo.module.push({
                                id: temp + j + 2,
                                name: this.selectInfo.setAllList[i].Children[j].ModuleName,
                                bk_module_id: this.selectInfo.setAllList[i].Children[j].ModuleID
                            })
                        }
                    }
                } else {
                    for (let i = 0; i < this.selectInfo.setAllList.length; i++) {
                        if (data.bk_set_id === this.selectInfo.setAllList[i].SetID) {
                            this.selectInfo.module.push({
                                id: 1,
                                name: this.$t('m.otherWord.all'),
                                bk_module_id: ''
                            })
                            for (let j = 0; j < this.selectInfo.setAllList[i].Children.length; j++) {
                                this.selectInfo.module.push({
                                    id: j + 2,
                                    name: this.selectInfo.setAllList[i].Children[j].ModuleName,
                                    bk_module_id: this.selectInfo.setAllList[i].Children[j].ModuleID
                                })
                            }
                            break
                        }
                    }
                }
            },
            getCloudList () {
                // 获取云区域数据
                let appId = this.appId
                if (!appId) { return }
                this.$store.dispatch('stall/getCloudInfo', {appId}).then((res) => {
                    this.selectInfo.cloudArea = []
                    this.selectInfo.cloudArea.push({
                        id: 1,
                        name: this.$t('m.tabControl.directArea'),
                        bk_cloud_id: '0'
                    })
                    for (let i = 0; i < res.data.length; i++) {
                        this.selectInfo.cloudArea.push({
                            id: i + 2,
                            name: res.data[i].bk_cloud_name,
                            bk_cloud_id: res.data[i].bk_cloud_id
                        })
                    }
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            // 获取操作系统类型
            getOperatType () {
                this.$store.dispatch('plug/getOperatType').then((res) => {
                    this.selectInfo.system = []
                    this.selectInfo.system.push({
                        id: 1,
                        name: this.$t('m.otherWord.all'),
                        type: ''
                    })
                    for (let i = 0; i < res.data.length; i++) {
                        this.selectInfo.system.push({
                            id: i + 2,
                            name: res.data[i].name,
                            type: res.data[i].id
                        })
                    }
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            // 查询信息
            selectSet (id, data) {
                // 查询Set, 联动查找模块数据
                this.searchInfo.setInfo = data.bk_set_id

                this.selectInfo.module = []
                this.selectInfo.moduleSelected = 0
                this.searchInfo.moduleInfo = ''

                this.getModuleList(data)
            },
            selectModule (id, data) {
                // 查询模块信息
                this.searchInfo.moduleInfo = data.bk_module_id
            },
            selectCloud (id, data) {
                // 查询云区域信息
                this.searchInfo.cloudInfo = data.bk_cloud_id
            },
            // 显示运行节点日志弹框
            showSlider (item, index) {
                this.cmdbSettings.isShow = !this.cmdbSettings.isShow
                let appId = this.appId
                let id = item.id
                this.logId = id
                this.$store.dispatch('stall/getStepInfo', {appId, id}).then((res) => {
                    this.cmdbSettings.info = res.data.logs
                }, res => {
                    this.cmdbSettings.info = res.data.msg
                })
                this.logSetInterval()
            },
            logSetInterval () {
                let appId = this.appId
                let id = this.logId
                this.stepInterval = setInterval(() => {
                    this.$store.dispatch('stall/getStepInfo', {appId, id}).then((res) => {
                        this.cmdbSettings.info = res.data.logs
                        document.getElementsByClassName('bk-sideslider-wrapper')[0].scrollTop = document.getElementsByClassName('bk-open-window')[0].offsetHeight
                        if (res.data.status === 'FAILED' || res.data.status === 'SUCCESS' || !this.cmdbSettings.isShow) {
                            clearInterval(this.stepInterval)
                        }
                    }, res => {
                        clearInterval(this.stepInterval)
                    })
                }, 2000)
            },
            // 勾选
            checkAll () {
                this.allCheck = !this.allCheck
                for (let i = 0; i < this.tabList.length; i++) {
                    this.tabList[i].checkStatus = this.allCheck
                    if (this.tabList[i].disInfo || this.tabList[i].stateInfomation.agentSta !== 'success') {
                        this.tabList[i].checkStatus = false
                    }
                }
                this.tabList = JSON.parse(JSON.stringify(this.tabList))
                if (this.allCheck) {
                    for (let i = 0; i < this.tabList.length; i++) {
                        let val = true
                        for (let j = 0; j < this.checkList.length; j++) {
                            if (this.tabList[i].id === this.checkList[j].id) {
                                val = false
                                break
                            }
                        }
                        if (val) {
                            this.checkList.push(this.tabList[i])
                        }
                    }
                } else {
                    for (let i = this.checkList.length - 1; i >= 0; i--) {
                        for (let j = 0; j < this.tabList.length; j++) {
                            if (this.checkList[i] && this.checkList[i].id === this.tabList[j].id) {
                                this.checkList.splice(i, 1)
                            }
                        }
                    }
                }
                for (let i = this.checkList.length - 1; i >= 0; i--) {
                    if (this.checkList[i] && (this.checkList[i].disInfo || this.checkList[i].stateInfomation.agentSta !== 'success')) {
                        this.checkList.splice(i, 1)
                    }
                }
            },
            checkOneStatus (item, index) {
                if (item.disInfo) { return }
                item.checkStatus = !item.checkStatus
                this.tabList = JSON.parse(JSON.stringify(this.tabList))
                this.allCheck = !(this.tabList.some(item => !item.checkStatus))
                if (item.checkStatus) {
                    this.checkList.push(item)
                } else {
                    for (let i = 0; i < this.checkList.length; i++) {
                        if (item.id === this.checkList[i].id) {
                            this.checkList.splice(i, 1)
                        }
                    }
                }
            },
            // 查看详情
            seeMoreInfo (item, index) {
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
            },
            // 下一步
            nextStep () {
                if (!this.checkList.length) { return }
                let systemInfo = this.checkList[0].os_type
                for (let i = 0; i < this.checkList.length; i++) {
                    if (systemInfo !== this.checkList[i].os_type) {
                        this.$bkMessage({
                            message: this.$t('m["不能同时对不同操作系统的主机进行操作"]'),
                            theme: 'warning'
                        })
                        return
                    }
                }

                this.ipInfo = {
                    bk_cloud_id: '2',
                    system: systemInfo,
                    hosts: []
                }
                this.ipInfo.bk_cloud_id = this.searchInfo.cloudInfo
                for (let i = 0; i < this.checkList.length; i++) {
                    this.ipInfo.hosts.push({
                        conn_ips: this.checkList[i].conn_ip
                    })
                }
                // 显示树的形态
                this.treeStatus = {
                    hostShow: false,
                    typeShow: true,
                    taskShow: false
                }
                this.stepInfo[0].complete = true
                this.stepInfo[1].complete = true
                this.stepInfo[2].complete = false
            },
            changeTree () {
                // 显示树的形态
                this.treeStatus = {
                    hostShow: false,
                    typeShow: false,
                    taskShow: true
                }
                this.stepInfo[0].complete = true
                this.stepInfo[1].complete = true
                this.stepInfo[2].complete = true
            },
            // 原始数形态
            originalTree () {
                // 显示树的形态
                this.treeStatus = {
                    hostShow: true,
                    typeShow: false,
                    taskShow: false
                }
                this.stepInfo[0].complete = true
                this.stepInfo[1].complete = false
                this.stepInfo[2].complete = false
            }
        }
    }
</script>
<style lang="scss" scoped>
    @import '../../scss/mixins/clearfix.scss';
    @import '../../scss/mixins/scroller.scss';

    .bk-plug {
        min-width: 1280px;
        margin: 0 auto;
        padding-top: 50px;
        padding-bottom: 100px;
    }
    .bk-plug-step {
        height: 60px;
        line-height: 60px;
        border-bottom: 1px solid #dde4eb;
        background-color: #fff;
        position: fixed;
        width: 100%;
        z-index: 100;
        ul {
            @include clearfix;
            width: 820px;
            position: relative;
            left: 50%;
            transform: translateX(-50%);
            li {
                float: left;
                @include clearfix;
                color: #ccd5dd;
                font-size: 12px;
                font-weight: bold;
                .bk-step-num {
                    float: left;
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    border: 1px solid #ccd5dd;
                    text-align: center;
                    line-height: 28px;
                    margin-top: 15px;
                    margin-right: 10px;
                }
                .bk-complete-border {
                    border: 1px solid #3e94ff;
                }
                .bk-step-info {
                    float: left;
                }
                .bk-step-interval {
                    float: left;
                    line-height: 53px;
                    padding: 0 100px;
                }
            }
            .bk-step-complete {
                color: #3e94ff;
            }
        }
    }
    .bk-plug-search {
        /*height: 54px;*/
        padding: 14px 20px;
        background-color: #fdfdfe;
        @include clearfix;
        .bk-form-item {
            float: left;
            margin-top: 0;
            width: 24%;
            padding-right: 20px;
            margin-right: 0px;
            .bk-label {
                float: left;
                line-height: 25px;
                font-size: 12px;
                color: #737987;
            }
            .ip-wrapper {
                position: relative;
                textarea {
                    height: 25px;
                    padding: 0px;
                    min-height: 25px;
                    position: absolute;
                    width: 100%;
                    background-color: #fdfdfe;
                    z-index: 100;
                    @include scroller;
                    &:focus {
                        height: 76px;
                        overflow: auto;
                    }
                }
            }
            .bk-form-content {
                float: left;
                width: 77%;
                input {
                    height: 25px;
                }
                .bk-form-input {
                    height: 25px;
                }
            }
        }
        .bk-form-btn {
            float: right;
            width: 4%;
            button {
                width: 100%;
                height: 25px;
            }
        }
    }
    .bk-tab-info {
        .bk-tab-head {
            >ul {
                @include clearfix;
                background-color: #fafbfd;
                border: 1px solid #dde4eb;
                >li {
                    float: left;
                    font-size: 12px;
                    font-weight: bold;
                    color: #737987;
                    width: 11%;
                    line-height: 40px;
                    text-align: left;
                    position: relative;
                    z-index: 10;
                    padding-left: 10px;
                    &:hover {
                        background-color: #ebf0f9;
                        .bk-tab-parent {
                            color: #3c96ff;
                        }
                    }
                    .bk-select-more {
                        position: absolute;
                        top: 40px;
                        left: 0;
                        width: 100%;
                        max-height: 162px;
                        border: 1px solid #c3cdd7;
                        background-color: #fff;
                        box-shadow: 0 0 1px 1px rgba(0,0,0,0.1);
                        >ul {
                            width: 100%;
                            max-height: 162px;
                            >li {
                                padding: 0 10px;
                                line-height: 30px;
                                font-size: 12px;
                                font-weight: normal;
                                cursor: pointer;
                                &:hover {
                                    background-color: #eef6fe;
                                    color: #3c96ff;
                                }
                            }
                            .bk-click-info {
                                background-color: #eef6fe;
                                color: #3c96ff;
                            }
                        }
                    }
                }
                .bk-tab-icon {
                    font-size: 12px;
                }
                .bk-cursor {
                    cursor: pointer;
                }
                .bk-blue-color {
                    color: #3c96ff;
                }
                .bk-head-type {
                    width: 18%;
                    padding-left: 72px;
                }
                .bk-head-ip {
                    width: 16%;
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
                        padding-left: 10px;
                        float: left;
                        width: 11%;
                        text-align: left;
                        position: relative;
                        border-bottom: 1px solid #dde4eb;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                        position: relative;
                        .bk-splice-icon {
                            position: absolute;
                            top: 0;
                            left: 35px;
                            cursor: pointer;
                            .icon-angle-down {
                                color: #3e94ff;
                            }
                        }
                        .bk-image-order {
                            position: absolute;
                            top: 12px;
                            right: 24px;
                            width: 20px;
                            height: 20px;
                            vertical-align: middle;
                            color: #3e94ff;
                            cursor: pointer;
                        }
                    }
                    .bk-node-squear {
                        position: absolute;
                        top: 15px;
                        left: 10px;
                        width: 12px;
                        height: 12px;
                        background-color: #fff;
                        border: 2px solid #30d878;
                        border-radius: 50%;
                    }
                    .bk-none-agent {
                        color: #c3cdd7!important;
                    }
                    .bk-squera-normal {
                        border: 2px solid #c3cdd7!important;
                    }
                    .bk-squera-error {
                        border: 2px solid #ff5757!important;
                    }
                    .bk-squera-primary {
                        border: 2px solid #3c96ff!important;
                    }
                    .bk-squera {
                        margin-left: 20px;
                    }
                    .bk-more-info {
                        position: absolute;
                        top: 44px;
                        left: 0;
                        padding: 0 65px;
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
                        }
                    }
                    .bk-body-click {
                        background-color: #ebf0f9;
                    }
                    .bk-ip-info {
                        line-height: 22px;
                        display: block;
                        height: 22px;
                    }
                    .bk-body-type {
                        width: 18%;
                        padding-left: 72px;
                    }
                    .bk-body-ip {
                        width: 16%;
                    }
                    &.bk-open-li {
                        height: 130px;
                        border-bottom: 1px solid #dde4eb;
                    }
                }
            }
        }
    }
    .bk-plug-button {
        text-align: center;
        margin-top: 25px;
        button {
            width: 100px;
            height: 36px;
        }
    }
    /*
    ** 分页
    */
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
    .bk-change-all {
        float: left;
        line-height: 46px;
        margin-left: 18px;
    }
    /*
    ** 暂无数据
    */
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
    /*
    ** 详细安装步骤
    */
    .bk-install-step {
        .bk-step-info {
            font-size: 12px;
            line-height: 20px;
            overflow: hidden;
        }
    }

    .moreInfo-enter-active {
        transition: max-height .2s ease;
    }
    .moreInfo-enter,.moreInfo-leave-active {
        max-height: 0px!important;
    }
    .moreInfo-leave,.moreInfo-enter-active {
        max-height: 162px;
    }
</style>
