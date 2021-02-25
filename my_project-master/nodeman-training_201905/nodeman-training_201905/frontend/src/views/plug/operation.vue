<template>
	<div class="bk-plug-operation">
        <div class="bk-operat-nav">
            <ul>
                <li v-for="(item, index) in navBar" :class="{'bk-li-click': item.complete}" @click="changeNav(item, index)">
                    <span>{{item.name}}</span>
                </li>
            </ul>
        </div>
        <!-- <div>{{ipInfo}}</div> -->
        <!-- 进程管理 -->
        <div class="bk-operat-process" v-if="navBar[0].complete" v-bkloading="{isLoading: isDataLoading}">
            <div class="bk-process-info">
                <div class="bk-process-operation">
                    <div class="bk-operation-left">
                        <span>{{$t('m["选择操作"]')}}：</span>
                    </div>
                    <div class="bk-operation-right">
                        <ul>
                            <li v-for="(item, index) in process.operationList" :class="{'bk-operation-click': item.complete, 'bk-none-border': index > 4}" @click="changeOperation(item, index)">
                                <span>{{item.name}}</span>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="bk-process-operation">
                    <div class="bk-operation-left">
                        <span>{{$t('m["插件类型"]')}}：</span>
                    </div>
                    <div class="bk-operation-right">
                        <bk-selector
                            :list="process.pluginTypeList"
                            :selected.sync="process.pluginTypeSelected"
                            @item-selected="changePluginType">
                        </bk-selector>
                    </div>
                </div>
                <div class="bk-process-operation">
                    <div class="bk-operation-left">
                        <span>{{$t('m["选择插件"]')}}：</span>
                    </div>
                    <div class="bk-operation-right">
                        <ul>
                            <li v-for="(item, index) in process.pluginList" :class="{'bk-operation-click': item.complete, 'bk-operation-disabled': item.disabled, 'bk-none-border': index > 4}" @click="changePlugin(item, index)">
                                <span>{{item.name}}</span>
                            </li>
                        </ul>
                        <div class="bk-right-info" v-if="process.completeCheck">
                            <span class="bk-info-icon">！</span>
                            <span>
                                <span style="margin-right: 14px">{{process.plugInfo.name}}</span>{{process.plugInfo.details}}
                            </span>
                        </div>
                        <div class="bk-right-none" v-else></div>
                    </div>
                </div>
            </div>
        </div>
        <!-- 插件更新 -->
        <div class="bk-operat-process" v-if="navBar[1].complete">
            <div class="bk-process-info">
                <div class="bk-process-operation">
                    <div class="bk-operation-left">
                        <span>{{$t('m["选择要变更的服务"]')}}：</span>
                    </div>
                    <div class="bk-operation-right">
                        <bk-selector
                            :list="pluginUpload.serviceList"
                            :selected.sync="pluginUpload.serviceSelected"
                            :disabled="pluginUpload.serviceDisabled">
                        </bk-selector>
                    </div>
                </div>
                <div class="bk-process-operation">
                    <div class="bk-operation-left">
                        <span>{{$t('m["插件类型"]')}}：</span>
                    </div>
                    <div class="bk-operation-right">
                        <bk-selector
                            :list="process.pluginTypeList"
                            :selected.sync="process.pluginTypeSelected"
                            @item-selected="changePluginType">
                        </bk-selector>
                    </div>
                </div>
                <div class="bk-process-operation">
                    <div class="bk-operation-left">
                        <span>{{$t('m["选择要更新的插件"]')}}：</span>
                    </div>
                    <div class="bk-operation-right">
                        <ul>
                            <li v-for="(item, index) in process.pluginList" :class="{'bk-operation-click': item.complete, 'bk-operation-disabled': item.disabled, 'bk-none-border': index > 4}" @click="changePlugin(item, index)">
                                <span>{{item.name}}</span>
                            </li>
                        </ul>
                        <div class="bk-right-info" v-if="process.completeCheck">
                            <span class="bk-info-icon">！</span>
                            <span>
                                <span style="margin-right: 14px">{{process.plugInfo.name}}</span>{{process.plugInfo.details}}
                            </span>
                        </div>
                    </div>
                </div>
                <div class="bk-process-operation">
                    <div class="bk-operation-left">
                        <span>{{$t('m["选择新包"]')}}：</span>
                    </div>
                    <div class="bk-operation-right">
                        <bk-selector
                            :list="pluginUpload.newPackageList"
                            :selected.sync="pluginUpload.packageSelected"
                            @item-selected="changePackage">
                        </bk-selector>
                        <div class="bk-package-prompt">
                            <p>
                                <p>{{$t('m["请联系运维"]')}}：</p>
                                <p>{{$t('m["将插件包上传到中控机的/data/src/目录并解压"]')}}</p>
                                <p>{{$t('m["然后执行./bkeec pack gse_plugin 更新插件信息到/data/src下"]')}}</p></p>
                            <span class="bk-prompt-square"></span>
                        </div>
                        <div class="bk-right-info" v-if="pluginUpload.packageSelected !== 0">
                            <span class="bk-info-icon">！</span>
                            <span>
                                <span>M D 5 {{$t('m["值"]')}}:<span style="margin-left: 10px">{{pluginUpload.packageInfo.mdFive}}</span></span></br>
                                <span>{{$t('m.headTab.updateTime')}}:<span style="margin-left: 10px" v-html="pluginUpload.packageInfo.uploadTime"></span></span>
                            </span>
                        </div>
                        <div class="bk-right-checkbox">
                            <form class="bk-form">
                                <div class="bk-form-item">
                                    <div class="bk-form-content" style="margin-left: 0px;" v-for="(node, index) in pluginUpload.packageCheckList">
                                        <label class="bk-form-checkbox bk-checkbox-small">
                                            <input type="checkbox" name="checkPackage" :checked="node.checkStatus" @click="checkPackage(node, index)">
                                            <i class="bk-checkbox-text" >{{node.name}}</i>
                                        </label>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
                <!-- <div class="bk-process-operation">
                    <div class="bk-operation-left">
                        <span>更新类型：</span>
                    </div>
                    <div class="bk-operation-right">
                        <bk-selector
                            :list="pluginUpload.uploadTypeList"
                            :selected.sync="pluginUpload.uploadTypeSelected"
                            @item-selected="changeUploadType">
                        </bk-selector>
                        <div class="bk-right-info" v-if="pluginUpload.uploadTypeSelected !== 0">
                            <span class="bk-info-icon">！</span>
                            <span>
                                <span>删除掉同目录下的所有文件. 用选择的包内容完全替换</span>
                            </span>
                        </div>
                    </div>
                </div> -->
            </div>
        </div>
        <!-- 配置更新 -->
        <!-- <div class="bk-operat-process" v-if="navBar[2].complete">
            <div class="bk-process-info">
                <div class="bk-process-operation">
                    <div class="bk-operation-left">
                        <span>选择要变更的服务：</span>
                    </div>
                    <div class="bk-operation-right">
                        <bk-selector
                            :list="pluginUpload.serviceList"
                            :selected.sync="pluginUpload.serviceSelected"
                            :disabled="pluginUpload.serviceDisabled">
                        </bk-selector>
                    </div>
                </div>
                <div class="bk-process-operation">
                    <div class="bk-operation-left">
                        <span>插件类型：</span>
                    </div>
                    <div class="bk-operation-right">
                        <bk-selector
                            :list="process.pluginTypeList"
                            :selected.sync="process.pluginTypeSelected"
                            @item-selected="changePluginType">
                        </bk-selector>
                    </div>
                </div>
                <div class="bk-process-operation">
                    <div class="bk-operation-left">
                        <span>选择插件：</span>
                    </div>
                    <div class="bk-operation-right">
                        <ul>
                            <li v-for="(item, index) in process.pluginList" :class="{'bk-operation-click': item.complete, 'bk-operation-disabled': item.disabled, 'bk-none-border': index > 4}" @click="changePlugin(item, index)">
                                <span>{{item.name}}</span>
                            </li>
                        </ul>
                        <div class="bk-right-info" v-if="process.completeCheck">
                            <span class="bk-info-icon">！</span>
                            <span>
                                <span style="margin-right: 14px">{{process.plugInfo.name}}</span>{{process.plugInfo.details}}
                            </span>
                        </div>
                    </div>
                </div>
                <div class="bk-process-operation">
                    <div class="bk-operation-left">
                        <span>配置文件格式：</span>
                    </div>
                    <div class="bk-operation-right">
                        <div class="bk-right-checkbox">
                            <form class="bk-form">
                                <div class="bk-form-item">
                                    <div class="bk-form-content" style="margin-left: 0px; float: left;" v-for="(node, index) in configuUpload.fileFormat">
                                        <label class="bk-form-radio bk-radio-small">
                                            <input type="radio" name="fileFornat" :checked="node.checkStatus" @click="checkFileFormat(node, index)">
                                            <i class="bk-radio-text" >{{node.name}}</i>
                                        </label>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
                <div class="bk-process-operation">
                    <div class="bk-operation-left">
                        <span>上传文件：</span>
                    </div>
                    <div class="bk-operation-right">
                        <div class="bk-right-file">
                            <input type="file" class="bk-file-info">
                            <div class="bk-file-style">
                                <span>+ 点击上传或拖动文件到此处</span>
                                <div class="bk-file-change">
                                    <form class="bk-form">
                                        <div class="bk-form-item">
                                            <div class="bk-form-content" style="margin-left: 0px;">
                                                <label class="bk-form-checkbox bk-checkbox-small">
                                                    <input type="checkbox">
                                                    <i class="bk-checkbox-text">自动识别换行符</i>
                                                </label>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                                <div class="bk-file-success">
                                    <span>
                                        <span class="bk-file-icon"><i class="bk-icon icon-check-1"></i></span>
                                        <span>blueking-logo.kpi 上传成功</span></span>
                                    <span class="bk-see-more" @click="closeFile">点击预览</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div> -->
        <!-- 文件预览 -->
        <div class="bk-shade" v-if="fileInfo.showStatus">
            <div class="bk-file-more">
                <div class="bk-head">
                    <span>{{$t('m["文件预览"]')}}</span>
                    <span class="bk-head-close" @click="closeFile"><i class="bk-icon icon-close"></i></span>
                </div>
                <div class="bk-content">
                    <ul>
                        <li v-for="(item, index) in fileInfo.list">
                            <span>{{item.name}}</span>
                        </li>
                    </ul>
                </div>
                <div class="bk-file-btn">
                    <bk-button type="default" @click="closeFile">
                        {{$t('m["关闭"]')}}
                    </bk-button>
                </div>
            </div>
        </div>
        <div class="bk-process-btn">
            <bk-button type="default" @click="backPrevious" :disabled="secondClick">
                {{$t('m["上一步"]')}}
            </bk-button>
            <span style="margin-left: 20px"></span>
            <bk-button type="primary" @click="clickNext" :loading="secondClick">
                {{$t('m["立即执行"]')}}
            </bk-button>
        </div>
	</div>
</template>

<script>
    export default {
        props: {
            ipInfo: {
                type: Object,
                default () {
                    return {}
                }
            }
        },
        data () {
            return {
                isDataLoading: false,
                secondClick: false,
                navBar: [
                    {id: 1, name: this.$t('m["进程管理"]'), complete: true},
                    {id: 2, name: this.$t('m["插件更新"]'), complete: false}
                    // {id: 3, name: '配置更新', complete: false}
                ],
                // 进程管理
                process: {
                    operationList: [],
                    pluginTypeList: [],
                    pluginTypeSelected: 1,
                    pluginList: [
                        // {id: 1, name: 'basereport', complete: true, disabled: false},
                        // {id: 2, name: 'unifytlogc', complete: false, disabled: false},
                        // {id: 3, name: 'metricsbeat', complete: false, disabled: true},
                        // {id: 4, name: 'processbea', complete: false, disabled: false},
                        // {id: 6, name: 'bkdiscover', complete: false, disabled: false}
                    ],
                    completeCheck: false,
                    plugInfo: {
                        name: '',
                        details: ''
                    }
                },
                // 进程参数
                processForm: {
                    bk_cloud_id: '',
                    node_type: 'AGENT',
                    op_type: '',
                    global_params: {
                        plugin: {}
                    },
                    hosts: [{conn_ips: ''}]
                },
                // 插件更新
                plugForm: {
                    bk_cloud_id: '',
                    node_type: 'AGENT',
                    op_type: 'UPGRADE',
                    global_params: {
                        plugin: {},
                        package: {},
                        control: {},
                        option: {
                            keep_config: 0,
                            no_restart: 0,
                            no_delegate: 0
                        },
                        upgrade_type: 'APPEND'
                    },
                    hosts: [{conn_ips: ''}]
                },
                // 插件更新
                pluginUpload: {
                    serviceList: [
                        {id: 1, name: 'GSE ' + this.$t('m["插件"]')}
                    ],
                    serviceSelected: 1,
                    serviceDisabled: true,
                    // 选择新包
                    newPackageList: [],
                    packageSelected: 0,
                    packageInfo: {
                        mdFive: '',
                        uploadTime: ''
                    },
                    packageCheckList: [
                        {id: 1, name: this.$t('m["保留原有配置文件"]'), checkStatus: false},
                        {id: 2, name: this.$t('m["仅更新文件，不重启进程"]'), checkStatus: false}
                        // {id: 3, name: '下发后不托管', checkStatus: false}
                    ],
                    // 更新类型
                    uploadTypeList: [
                        {id: 1, name: this.$t('m["增量更新(仅覆盖)"]'), type: 'APPEND'},
                        {id: 2, name: this.$t('m["覆盖更新(先删除原目录后覆盖)"]'), type: 'OVERRIDE'}
                    ],
                    uploadTypeSelected: 1
                },
                // 配置更新
                configuUpload: {
                    fileFormat: [
                        {id: 1, name: 'yaml', checkStatus: true},
                        {id: 2, name: 'json', checkStatus: false},
                        {id: 3, name: 'ini', checkStatus: false}
                    ]
                },
                // 文件预览
                fileInfo: {
                    showStatus: false,
                    list: [
                        // {id: 1, name: '[10.0.2.76]20180424-161315 26   install cmdb  FATAL stat...  skip'},
                        // {id: 2, name: '[10.0.2.76]20180424-161315 26   install cmdb  FATAL stat...  skip'},
                        // {id: 3, name: '[10.0.2.76]20180424-161315 26   install cmdb  FATAL stat...  skip'}
                    ]
                }
            }
        },
        computed: {
            appId () {
                return this.$store.state.stall.appliId
            }
        },
        watch: {
            appId () {
                this.clearInfo()
                this.getOperatList()
                this.getPlufList()
            }
        },
        created () {
            this.getOperatList()
            this.getPlufList()
        },
        methods: {
            // 获取操作列表数据
            getOperatList () {
                this.isDataLoading = true
                this.$store.dispatch('plug/getOperatList').then((res) => {
                    this.process.operationList = res.data
                    for (let i = 0; i < this.process.operationList.length; i++) {
                        this.process.operationList[i].complete = false
                    }
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.isDataLoading = false
                })
            },
            // 获取插件分类
            getPlufList () {
                this.process.pluginTypeList = []
                this.$store.dispatch('plug/getPlugClassifi').then((res) => {
                    for (let i = 0; i < res.data.length; i++) {
                        this.process.pluginTypeList.push({
                            id: i + 1,
                            name: res.data[i].name,
                            info: res.data[i].id
                        })
                    }
                    if (!this.process.pluginTypeList.length) { return }
                    let value = this.process.pluginTypeList[0].info
                    this.getPlugInfo(value)
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            // 按分类获取插件列表
            getPlugInfo (value) {
                let params = value
                this.$store.dispatch('plug/getPlugInfo', {params}).then((res) => {
                    this.process.pluginList = res.data
                    for (let i = 0; i < this.process.pluginList.length; i++) {
                        this.process.pluginList[i].complete = false
                    }
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            // 按插件获取包
            getPackageList (value) {
                let params = value
                let info = this.ipInfo.system
                this.$store.dispatch('plug/getPackageList', {params, info}).then((res) => {
                    this.pluginUpload.newPackageList = res.data
                    for (let i = 0; i < this.pluginUpload.newPackageList.length; i++) {
                        this.pluginUpload.newPackageList[i].name = this.pluginUpload.newPackageList[i].pkg_name
                    }
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            // 选择导航类型
            changeNav (item, index) {
                for (let i = 0; i < this.navBar.length; i++) {
                    this.navBar[i].complete = false
                }
                this.navBar[index].complete = true
                this.process.completeCheck = false
                for (let i = 0; i < this.process.pluginList.length; i++) {
                    this.process.pluginList[i].complete = false
                }
                if (index === 1) {
                    this.pluginUpload.newPackageList = []
                    this.pluginUpload.packageSelected = 0
                }
                this.clearInfo()
            },
            clearInfo () {
                this.processForm = {
                    bk_cloud_id: '',
                    node_type: 'AGENT',
                    op_type: '',
                    global_params: {
                        plugin: {}
                    },
                    hosts: [{conn_ips: ''}]
                }
                this.plugForm = {
                    bk_cloud_id: '',
                    node_type: 'AGENT',
                    op_type: 'UPGRADE',
                    global_params: {
                        plugin: {},
                        package: {},
                        control: {},
                        option: {
                            keep_config: 0,
                            no_restart: 0,
                            no_delegate: 0
                        },
                        upgrade_type: 'APPEND'
                    },
                    hosts: [{conn_ips: ''}]
                }
                for (let i = 0; i < this.pluginUpload.packageCheckList.length; i++) {
                    this.pluginUpload.packageCheckList[i].checkStatus = false
                }
                this.pluginUpload.uploadTypeSelected = 1
            },
            // 进程管理
            // 选择操作
            changeOperation (item, index) {
                for (let i = 0; i < this.process.operationList.length; i++) {
                    this.process.operationList[i].complete = false
                }
                this.process.operationList[index].complete = true
                this.processForm.op_type = item.id
                this.process.operationList = JSON.parse(JSON.stringify(this.process.operationList))
            },
            // 插件类型
            changePluginType (id, data) {
                let value = data.info
                this.getPlugInfo(value)
                this.process.completeCheck = false
            },
            // 选择插件
            changePlugin (item, index) {
                if (item.disabled) { return }
                for (let i = 0; i < this.process.pluginList.length; i++) {
                    this.process.pluginList[i].complete = false
                }
                this.process.pluginList[index].complete = true
                this.process.pluginList = JSON.parse(JSON.stringify(this.process.pluginList))
                this.process.completeCheck = true
                this.process.plugInfo.name = item.name
                this.process.plugInfo.details = item.scenario
                // 插件信息
                this.processForm.global_params.plugin = item

                if (this.navBar[1].complete) {
                    let value = item.name
                    this.getPackageList(value)
                    // this.getRoadInfo(value)
                }
            },
            // 获取插件安装位置
            // getRoadInfo (value) {
            //     let params = value
            //     this.$store.dispatch('plug/getRoadInfo', {params}).then((res) => {
            //         this.plugForm.global_params.control = res.data
            //     }, res => {
            //         this.$bkMessage({
            //             message: res.data.msg,
            //             theme: 'error'
            //         })
            //     })
            // },
            // 插件更新
            // 选择新包
            changePackage (id, data) {
                this.pluginUpload.packageInfo.mdFive = data.md5
                this.pluginUpload.packageInfo.uploadTime = data.pkg_mtime

                this.plugForm.global_params.package = data
                // this.plugForm.global_params.package.id = data.id
                // this.plugForm.global_params.package.project = data.project
                // this.plugForm.global_params.package.pkg_name = data.pkg_name
            },
            // 选择包文件配置
            checkPackage (node, index) {
                node.checkStatus = !node.checkStatus
                this.pluginUpload.packageCheckList = JSON.parse(JSON.stringify(this.pluginUpload.packageCheckList))
            },
            // 更新类型
            changeUploadType (id, data) {
                this.plugForm.global_params.upgrade_type = data.type
            },
            // 配置更新
            // 配置文件格式
            checkFileFormat (node, index) {
                for (let i = 0; i < this.configuUpload.fileFormat.length; i++) {
                    this.configuUpload.fileFormat[i].checkStatus = false
                }
                this.configuUpload.fileFormat[index].checkStatus = true
                this.configuUpload.fileFormat = JSON.parse(JSON.stringify(this.configuUpload.fileFormat))
            },
            // 参数校验
            checkProcessInfo () {
                let msg = this.processForm.op_type ? (this.processForm.global_params.plugin.id ? '' : this.$t('m["请选择插件"]')) : this.$t('m["请选择操作"]')
                if (msg) {
                    this.$bkMessage({
                        message: msg,
                        theme: 'error'
                    })
                }
                return !!msg
            },
            // 进程管理操作
            processManage () {
                if (this.secondClick) { return }
                this.secondClick = true
                let params = {
                    bk_cloud_id: this.ipInfo.bk_cloud_id,
                    node_type: 'PLUGIN',
                    op_type: this.processForm.op_type,
                    global_params: {
                        plugin: this.processForm.global_params.plugin
                    },
                    hosts: this.ipInfo.hosts
                }
                let appId = this.appId
                this.uploadAjax(params, appId)
            },
            // 参数校验
            checkPlugInfo () {
                let msg = ''
                msg = this.processForm.global_params.plugin.id ? (this.pluginUpload.packageSelected !== 0 ? (this.pluginUpload.uploadTypeSelected !== 0 ? '' : this.$t('m["请选择更新类型"]')) : this.$t('m["请选择新包"]')) : this.$t('m["请选择插件"]')
                if (msg) {
                    this.$bkMessage({
                        message: msg,
                        theme: 'error'
                    })
                }
                return !!msg
            },
            // 插件更新
            plugUploadInfo () {
                if (this.secondClick) { return }
                this.secondClick = true
                this.plugForm.global_params.option.keep_config = this.pluginUpload.packageCheckList[0].checkStatus ? 1 : 0
                this.plugForm.global_params.option.no_restart = this.pluginUpload.packageCheckList[1].checkStatus ? 1 : 0
                this.plugForm.global_params.option.no_delegate = 0
                let params = {
                    bk_cloud_id: this.ipInfo.bk_cloud_id,
                    node_type: 'PLUGIN',
                    op_type: this.plugForm.op_type,
                    global_params: {
                        plugin: this.processForm.global_params.plugin,
                        package: this.plugForm.global_params.package,
                        // control: this.plugForm.global_params.control,
                        option: {
                            keep_config: this.plugForm.global_params.option.keep_config,
                            no_restart: this.plugForm.global_params.option.no_restart,
                            no_delegate: this.plugForm.global_params.option.no_delegate
                        },
                        upgrade_type: this.plugForm.global_params.upgrade_type
                    },
                    hosts: this.ipInfo.hosts
                }
                let appId = this.appId
                // this.uploadAjax(params, appId)
                this.splitPlug(params, appId)
            },
            splitPlug (params, appId) {
                this.$store.dispatch('plug/splitPlugInfo', {params, appId}).then((res) => {
                    for (let i = 0; i < res.data.length; i++) {
                        this.uploadAjax(res.data[i], appId)
                    }
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            uploadAjax (params, appId) {
                this.$store.dispatch('plug/processManga', {params, appId}).then((res) => {
                    let value = res.data.id
                    this.$store.commit('plug/changeJobId', value)
                    this.$parent.changeTree()
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.secondClick = false
                })
            },
            // 立即执行
            clickNext () {
                if (this.navBar[0].complete) {
                    if (this.checkProcessInfo()) { return }
                    this.processManage()
                }
                if (this.navBar[1].complete) {
                    if (this.checkPlugInfo()) { return }
                    this.plugUploadInfo()
                }
            },
            // 返回上一步
            backPrevious () {
                this.clearInfo()
                this.$parent.originalTree()
            },
            // 关闭文件预览
            closeFile () {
                this.fileInfo.showStatus = !this.fileInfo.showStatus
            }
        }
    }
</script>
<style lang="scss" scoped>
    @import '../../scss/mixins/clearfix.scss';
    @import '../../scss/mixins/scroller.scss';

    .bk-plug-operation {
        position: relative;
    }
    /* 头部导航 */
    .bk-operat-nav {
        ul {
            @include clearfix;
            padding: 0 35px;
            border-bottom: 1px solid #dde4eb;
            background-color: #fff;
            li {
                float: left;
                padding: 0 30px;
                line-height: 40px;
                font-size: 14px;
                color: #737987;
                cursor: pointer;
            }
            .bk-li-click {
                border-bottom: 2px solid #3c96ff;
                color: #3c96ff;
            }
        }
    }
    /* 进程管理 */
    .bk-operat-process {
        position: relative;
        padding: 50px 0px;
        background-color: #fff;
        border-bottom: 1px solid #dde4eb;
        .bk-process-info {
            position: relative;
            left: 50%;
            transform: translateX(-50%);
            width: 780px;
        }
        .bk-process-operation {
            @include clearfix;
            line-height: 36px;
            margin-bottom: 20px;
            .bk-operation-right {
                width: 600px;
                font-size: 14px;
                color: #737987;
                float: left;
                position: relative;
                ul {
                    @include clearfix;
                    li {
                        float: left;
                        width: 120px;
                        border: 1px solid #c3cdd7;
                        line-height: 34px;
                        border-right: none;
                        text-align: center;
                        cursor: pointer;
                        &:nth-child(5n) {
                            border-right: 1px solid #c3cdd7;
                        }
                        &:last-child {
                            border-right: 1px solid #c3cdd7;
                        }
                    }
                    .bk-operation-click {
                        background-color: #3c96ff;
                        border: none;
                        color: #fff;
                        line-height: 36px;
                    }
                    .bk-none-border {
                        border-top: none;
                    }
                    .bk-operation-disabled {
                        background-color: #fafbfd;
                        color: #dde4eb;
                        border-color: #dde4eb;
                        cursor: not-allowed;
                    }
                }
                .bk-right-info {
                    width: 100%;
                    padding: 10px;
                    background-color: #ebf4ff;
                    margin-top: 20px;
                    padding-left: 38px;
                    position: relative;
                    .bk-info-icon {
                        position: absolute;
                        top: 19px;
                        left: 14px;
                        width: 16px;
                        height: 16px;
                        text-align: center;
                        line-height: 16px;
                        background-color: #737987;
                        color: #fff;
                        font-size: 12px;
                        font-weight: bold;
                        border-radius: 50%;
                    }
                }
                .bk-right-none {
                    margin-top: 20px;
                    height: 56px;
                }
                .bk-right-file {
                    position: relative;
                    .bk-file-style {
                        width: 316px;
                        line-height: 34px;
                        border: 1px solid #c3cdd7;
                        text-align: center;
                        background-color: #fff;
                        color: #3c96ff;
                        cursor: pointer;
                        .bk-file-change {
                            position: absolute;
                            top: 0;
                            left: 336px;
                            input {
                                height: 14px!important;
                            }
                        }
                        .bk-file-success {
                            position: absolute;
                            top: 34px;
                            left: 0;
                            color: #737987;
                            .bk-see-more {
                                color: #3c96ff;
                                cursor: pointer;
                                margin-left: 20px;
                            }
                            .bk-file-icon {
                                display: inline-block;
                                width: 16px;
                                height: 16px;
                                border: 1px solid #55df90;
                                border-radius: 50%;
                                font-size: 12px;
                                color: #55df90;
                                text-align: center;
                                line-height: 15px;
                            }
                        }
                    }
                    .bk-file-info {
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 316px;
                        height: 36px;
                        opacity: 0;
                        cursor: pointer;
                    }
                }
                .bk-package-prompt {
                    position: absolute;
                    top: 0;
                    right: -245px;
                    font-size: 12px;
                    color: #fff;
                    background-color: #4c4c4c;
                    line-height: 20px;
                    width: 224px;
                    padding: 5px 10px;
                    .bk-prompt-square {
                        position: absolute;
                        top: 13px;
                        left: -5px;
                        width: 10px;
                        height: 10px;
                        background-color: #4c4c4c;
                        transform: rotate(45deg);
                    }
                }
            }
            .bk-operation-left {
                width: 180px;
                font-size: 14px;
                color: #737987;
                float: left;
                text-align: right;
                padding-right: 10px;
            }
        }
    }
    .bk-process-btn {
        text-align: center;
        margin-top: 20px;
        button {
            width: 100px;
            height: 36px;
            line-height: 36px;
        }
    }
    /* 弹窗 */
    .bk-shade {
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        display: table-cell;
        height: 100%;
        width: 100%;
        z-index: 2001;
        background-color: rgba(75,75,75,0.5);
    }
    .bk-file-more {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 740px;
        height: 780px;
        box-shadow: 0 0 7px 3px rgba(0, 0, 0, 0.1);
        border-radius: 2px;
        background-color: #fff;
        z-index: 2002;
        padding: 35px;
        .bk-head {
            text-align: center;
            font-size: 20px;
            color: #333;
            margin-bottom: 20px;
            position: relative;
            .bk-head-close {
                position: absolute;
                top: -18px;
                right: -18px;
                width: 24px;
                height: 24px;
                font-size: 14px;
                text-align: center;
                line-height: 14px;
                padding: 5px;
                color: #737987;
                cursor: pointer;
                &:hover {
                    background-color: #333;
                    color: #fff;
                    border-radius: 50%;
                }
            }
        }
        .bk-content {
            border: 1px solid #c3cdd7;
            height: 630px;
            overflow: auto;
            @include scroller;
            padding: 16px 24px;
            line-height: 26px;
            font-size: 12px;
            color: #737987;
        }
        .bk-file-btn {
            text-align: center;
            margin-top: 20px;
            button {
                width: 110px;
                height: 36px;
            }
        }
    }
</style>
