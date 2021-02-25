<template>
    <div class="bk-advanced-set">
        <h1 class="bk-set-h1">高级添加{{nodeType}}</h1>
        <div class="bk-advanced-info">
            <!-- 添加节点 -->
            <div class="bk-advanced-node">
                <ul>
                    <li v-for="(item, index) in alreadyNodeList" @click="seeNodeInfo(item, index)">
                        <div class="bk-add-head">
                            <div class="bk-node-ip">
                                <i class="bk-icon icon-right-shape"></i>
                                <span>{{item.loginIp}}</span>
                                <span>/{{item.communicationIp}}</span>
                                <span>/{{item.dataIp}}</span>
                                <span v-if="formInfo.type !== 'AGENT'">/{{item.cascadeIp}}</span> 
                            </div>
                            <span class="bk-node-operat">{{item.operat}}</span>
                            <span class="bk-node-method"
                                v-for="(authen, index) in authenticationList"
                                v-if="item.method === authen.id">
                                {{authen.name}}
                            </span>
                            <span class="bk-node-delete">
                                <i class="bk-icon icon-delete"
                                    @click.stop="deleteNode(item, index)"></i>
                                <div class="bk-delete-submit" v-if="item.showOpen">
                                    <span class="bk-delete-icon"></span>
                                    <span @click.stop="deleteSub">确认</span>
                                    <span @click.stop="deleteclose">取消</span>
                                </div>
                            </span>
                        </div>
                    </li>
                </ul>
            </div>
            <div class="bk-advanced-add">
                <ul>
                    <li>
                        <div class="bk-add-head" v-if="showNewTitle">添加新节点</div>
                        <div class="bk-add-form">
                            <form class="bk-form">
                                <div class="bk-form-item is-required">
                                    <label class="bk-label">节点类型：</label>
                                    <div class="bk-form-content" style="margin-left: 120px;">
                                        <bk-selector
                                            class="bk-style-width"
                                            :list="nodeTypeList"
                                            :selected.sync="formInfo.type"
                                            :disabled="true"
                                            @item-selected="selectedType">
                                        </bk-selector>
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label">登录IP：</label>
                                    <div class="bk-form-content" style="margin-left: 120px;">
                                        <input type="text" 
                                            class="bk-form-input bk-style-width" 
                                            v-model.trim="formInfo.loginIp" 
                                            :placeholder="placeInfo.loginIp">
                                        <div class="bk-cmdb">
                                            <label class="bk-form-checkbox bk-checkbox-small">
                                                <input 
                                                    type="checkbox" 
                                                    name="checkLogin"
                                                    :checked="toCmdbCheck.loginIp"
                                                    @click="changeToCmdbCheck('loginIp')">
                                                <i class="bk-checkbox-text">注册此IP到CMDB中</i>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label">通信IP：</label>
                                    <div class="bk-form-content" style="margin-left: 120px;">
                                        <input type="text" 
                                            class="bk-form-input bk-style-width" 
                                            v-model.trim="formInfo.communicationIp" 
                                            :placeholder="placeInfo.communicationIp">
                                        <div class="bk-cmdb">
                                            <label class="bk-form-checkbox bk-checkbox-small">
                                                <input 
                                                    type="checkbox" 
                                                    name="checkCommunication"
                                                    :checked="toCmdbCheck.communicationIp"
                                                    @click="changeToCmdbCheck('communicationIp')"
                                                    :disabled="true">
                                                <i class="bk-checkbox-text">注册此IP到CMDB中</i>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label">数据IP：</label>
                                    <div class="bk-form-content" style="margin-left: 120px;">
                                        <input type="text" 
                                            class="bk-form-input bk-style-width" 
                                            v-model.trim="formInfo.dataIp" 
                                            :placeholder="placeInfo.dataIp">
                                        <div class="bk-cmdb">
                                            <label class="bk-form-checkbox bk-checkbox-small">
                                                <input 
                                                    type="checkbox" 
                                                    name="checkData" 
                                                    :checked="toCmdbCheck.dataIp"
                                                    @click="changeToCmdbCheck('dataIp')">
                                                <i class="bk-checkbox-text">注册此IP到CMDB中</i>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                <div class="bk-form-item" v-if="formInfo.type !== 'AGENT'">
                                    <label class="bk-label">级联IP：</label>
                                    <div class="bk-form-content" style="margin-left: 120px;">
                                        <input type="text" 
                                            class="bk-form-input bk-style-width" 
                                            v-model.trim="formInfo.cascadeIp" 
                                            :placeholder="placeInfo.cascadeIp">
                                    </div>
                                </div>
                                <div class="bk-form-item is-required">
                                    <label class="bk-label">操作系统：</label>
                                    <div class="bk-form-content" style="margin-left: 120px;">
                                        <bk-selector
                                            class="bk-style-width"
                                            :list="operatList"
                                            :selected.sync="formInfo.operat"
                                            @item-selected="selectedOperat">
                                        </bk-selector>
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label">登录端口：</label>
                                    <div class="bk-form-content" style="margin-left: 120px;">
                                        <input type="text" 
                                            class="bk-form-input bk-style-width" 
                                            v-model.trim="formInfo.port" 
                                            placeholder="请输入登录端口">
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label">登录账号：</label>
                                    <div class="bk-form-content" style="margin-left: 120px;">
                                        <input type="text" 
                                            class="bk-form-input bk-style-width" 
                                            v-model.trim="formInfo.account" 
                                            placeholder="请输入登录账号">
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label">认证方式：</label>
                                    <div class="bk-form-content" style="margin-left: 120px;">
                                        <bk-selector
                                            class="bk-style-width"
                                            :list="authenticationList"
                                            :selected.sync="formInfo.method"
                                            @item-selected="selectedMethod">
                                        </bk-selector>
                                        <div class="bk-cmdb">
                                            <label class="bk-form-checkbox bk-checkbox-small">
                                                <input type="checkbox" name="checkMethod">
                                                <i class="bk-checkbox-text">加密保存认证信息</i>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                <div class="bk-form-item">
                                    <label class="bk-label">认证资料：</label>
                                    <template v-if="formInfo.method === 1">
                                        <div class="bk-form-content" style="margin-left: 120px;">
                                            <input type="password" 
                                                class="bk-form-input bk-style-width" 
                                                v-model.trim="formInfo.password" 
                                                placeholder="请输入密码">
                                        </div>
                                    </template>
                                    <template v-else>
                                        <div class="bk-form-content" 
                                            style="margin-left: 120px;">
                                            <bk-button 
                                                v-if="!formInfo.name"
                                                type="default" 
                                                title="点击上传密钥文件" 
                                                class="bk-file-btn">
                                                <i class="bk-icon icon-save" style="margin-right: 10px;"></i>点击上传密钥文件
                                                <input type="file" class="bk-input-file" @change="readFile($event)">
                                            </bk-button>
                                            <div class="bk-file-message" v-else>
                                                <span>密钥文件</span>
                                                <span style="margin-left: 10px;">
                                                    <i class="bk-icon icon-order"></i>
                                                    <span style="color: #3C96FF;">{{formInfo.name}}</span>
                                                </span>
                                                <span style="margin-left: 10px; font-size: 12px; cursor: pointer;"
                                                    @click="closeFile">
                                                    <i class="bk-icon icon-close"></i>
                                                </span>
                                            </div>
                                        </div>
                                        <div class="bk-form-content" 
                                            style="margin-left: 120px; margin-top: 20px;"
                                            v-if="formInfo.method === 3">
                                            <bk-button type="default" title="点击上传证书文件" class="bk-file-btn">
                                                <i class="bk-icon icon-save" style="margin-right: 10px;"></i>点击上传证书文件
                                                <input type="file" class="bk-input-file">
                                            </bk-button>
                                        </div>
                                    </template>
                                </div>
                            </form>
                            <div class="bk-add-btn">
                                <bk-button 
                                    style="width: 140px; height: 36px;"
                                    type="primary" 
                                    title="添加新节点"
                                    @click="submitInfo">
                                    添加新节点
                                </bk-button>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
            <!-- 注意事项 -->
            <div class="bk-advanced-attention">
                <div class="bk-attention-head">注意事项：</div>
                <div class="bk-attention-package">
                    <p>Agent 服务器需要满足以下条件：</p> 
                    <p>1. APPO 所在机器(在 app 运行所在机器) 必须能通过 ssh 登陆到 Agent 机器 </p>
                    <p>2. Agent 所在机器可以访问到 zk 的端口</p> 
                    <p>3. 支持 Linux/Windows/AIX 操作系统</p> 
                    <p>4. Windows 服务器如果没有安装 Cygwin， 则需要开通139, 445端口 </p>
                    <p>5. 必须使用 root/Administrator 账户</p>
                </div>
            </div>
        </div>
        <div class="bk-advanced-btn">
            <bk-button 
                type="primary" 
                title="开始安装" 
                @click="addAreaAgentInfo">
                开始安装
            </bk-button>
            <bk-button 
                type="default" 
                title="仅导入机器" 
                @click="addAreaOtherInfo">
                仅导入机器
            </bk-button>
            <bk-button 
                type="default" 
                title="取消"
                @click="advancedInfo">
                取消
            </bk-button>
        </div>
    </div>
</template>
<script>
    export default {
        data () {
            return {
                isSaving: false,
                formInfo: {
                    type: '',
                    loginIp: '',
                    communicationIp: '',
                    dataIp: '',
                    cascadeIp: '',
                    operat: 'Linux',
                    osType: 'LINUX',
                    port: '',
                    account: '',
                    method: 1,
                    methodInfo: 'PASSWORD',
                    password: '',
                    key: '',
                    name: ''
                },
                // 新增节点
                addNewNode: true,
                showNewTitle: true,
                // 删除节点数据
                deleteInfo: {
                    info: '',
                    index: ''
                },
                // 已添加的节点
                alreadyNodeList: [
                    // {loginIp: '2.2.4.6', communicationIp: '2.3.5.4', dataIp: '10.208.57.142', cascadeIp: '', operat: 'Windows', method: '密码验证', showOpen: false}
                ],
                seeIndex: '',
                // 节点类型
                nodeTypeList: [
                    {id: 'AGENT', name: 'Agent'},
                    {id: 'PROXY', name: 'Proxy'},
                    {id: 'PAGENT', name: 'P-Agent'}
                ],
                placeInfo: {
                    loginIp: '',
                    communicationIp: '',
                    dataIp: '',
                    cascadeIp: ''
                },
                // 操作系统
                operatList: [
                    {id: 'Linux', name: 'Linux', type: 'LINUX'},
                    {id: 'Windows', name: 'Windows', type: 'WINDOWS'},
                    {id: 'WindowsCygwin', name: 'WindowsCygwin', type: 'WINDOWS'},
                    {id: 'AIX', name: 'AIX', type: 'AIX'}
                ],
                // 认证方式
                authenticationList: [
                    {id: 1, name: '密码认证', type: 'PASSWORD'},
                    {id: 2, name: '密钥认证', type: 'KEY'}
                    // {id: 3, name: '密钥+证书认证', type: 'PASSKEY'}
                ],
                // 注册IP到cmdb
                toCmdbCheck: {
                    loginIp: false,
                    communicationIp: true,
                    dataIp: false
                },
                // 上传文件
                fileInfo: ''
            }
        },
        props: {
            nodeType: {
                type: String,
                default () {
                    return ''
                }
            },
            cloudId: {
                type: String,
                default () {
                    return ''
                }
            },
            appId: {
                type: [String, Number],
                default: ''
            }
        },
        computed: {
            
        },
        mounted () {
            this.formInfo.type = this.nodeType
            this.nodePlace(this.formInfo.type)
        },
        methods: {
            // 节点类型不同提示不同的信息
            nodePlace (type) {
                if (type === 'AGENT' || type === 'PROXY') {
                    this.placeInfo = {
                        loginIp: '填写从APPO登录时，所使用的目标机器IP',
                        communicationIp: '启动Agent后，用于与Server端建立连接的本机网卡IP',
                        dataIp: '上报数据绑定的IP，将被注册到CMDB中',
                        cascadeIp: '被p-agent连接的proxy IP'
                    }
                } else if (type === 'PAGENT') {
                    this.placeInfo = {
                        loginIp: '填写从Proxy登录时，所使用的目标机器IP',
                        communicationIp: '启动Agent后，用于与Proxy建立连接的本机网卡IP',
                        dataIp: '上报数据绑定的IP，将被注册到CMDB中',
                        cascadeIp: '上一级proxy IP'
                    }
                }
            },
            // 查看节点信息
            seeNodeInfo (item, index) {
                for (let key in item) {
                    for (let val in this.formInfo) {
                        if (key === val) {
                            this.formInfo[val] = item[key]
                        }
                    }
                }
                this.seeIndex = index
                this.showNewTitle = false
                this.toCmdbCheck = {
                    loginIp: item.toCmdbCheck.loginIp,
                    communicationIp: item.toCmdbCheck.communicationIp,
                    dataIp: item.toCmdbCheck.dataIp
                }
            },
            // 删除节点
            deleteNode (item, index) {
                for (let i = 0; i < this.alreadyNodeList.length; i++) {
                    this.alreadyNodeList[i].showOpen = false
                }
                this.alreadyNodeList[index].showOpen = true
                this.alreadyNodeList = JSON.parse(JSON.stringify(this.alreadyNodeList))
                this.deleteInfo.info = item
                this.deleteInfo.index = index
            },
            deleteSub () {
                this.alreadyNodeList.splice(this.deleteInfo.index, 1)
            },
            deleteclose () {
                for (let i = 0; i < this.alreadyNodeList.length; i++) {
                    this.alreadyNodeList[i].showOpen = false
                }
                this.alreadyNodeList = JSON.parse(JSON.stringify(this.alreadyNodeList))
            },
            // 节点类型
            selectedType (id, data) {
                this.formInfo.type = id
                this.nodePlace(this.formInfo.type)
            },
            // 操作系统
            selectedOperat (id, data) {
                this.formInfo.operat = id
                this.formInfo.osType = data.type
            },
            // 认证方式
            selectedMethod (id, data) {
                this.formInfo.method = id
                this.formInfo.key = ''
                this.formInfo.password = ''
                this.formInfo.name = ''
            },
            // 注册IP到CMDB
            changeToCmdbCheck (type) {
                if (type === 'loginIp') {
                    this.toCmdbCheck.loginIp = !this.toCmdbCheck.loginIp
                } else if (type === 'dataIp') {
                    this.toCmdbCheck.dataIp = !this.toCmdbCheck.dataIp
                }
            },
            // 保存信息
            submitInfo () {
                if (this.changeInput()) { return }
                let nodeInfo = this.formInfo
                nodeInfo.showOpen = false
                nodeInfo.toCmdbCheck = {
                    loginIp: this.toCmdbCheck.loginIp,
                    communicationIp: this.toCmdbCheck.communicationIp,
                    dataIp: this.toCmdbCheck.dataIp
                }
                if (this.showNewTitle) {
                    this.alreadyNodeList.push(nodeInfo)
                } else {
                    this.alreadyNodeList.splice(this.seeIndex, 1, nodeInfo)
                }
                this.showNewTitle = true
                this.seeIndex = ''
                this.clearInfo()
            },
            changeInput () {
                let valList = [
                    {name: '请输入登陆Ip', type: 'loginIp', check: false},
                    {name: '请输入通信Ip', type: 'communicationIp', check: false},
                    {name: '请输入数据Ip', type: 'dataIp', check: false},
                    {name: '请输入级联Ip', type: 'cascadeIp', check: false},
                    {name: '请输入登录端口', type: 'port', check: false},
                    {name: '请输入登录账号', type: 'account', check: false},
                    {name: '请输入密码', type: 'password', check: false},
                    {name: '请上传密钥', type: 'key', check: false}
                ]
                valList[3].check = this.nodeType === 'AGENT'
                valList[6].check = this.formInfo.method === 2
                valList[7].check = this.formInfo.method === 1
                for (let i = 0; i < valList.length; i++) {
                    for (let key in this.formInfo) {
                        if (valList[i].type === key && !valList[i].check && !this.formInfo[key]) {
                            this.$bkMessage({
                                message: valList[i].name,
                                theme: 'error'
                            })
                            return true
                        }
                    }
                }
                return false
            },
            clearInfo () {
                this.formInfo = {
                    type: this.nodeType,
                    loginIp: '',
                    communicationIp: '',
                    dataIp: '',
                    cascadeIp: '',
                    operat: 'Linux',
                    osType: 'LINUX',
                    port: '',
                    account: '',
                    method: 1,
                    methodInfo: 'PASSWORD',
                    password: '',
                    key: '',
                    name: ''
                }
                this.toCmdbCheck = {
                    loginIp: false,
                    communicationIp: true,
                    dataIp: false
                }
            },
            readFile ($event) {
                this.fileInfo = $event.target.files[0]
                if (this.fileInfo.size / 1024 >= 30000) {
                    this.$bkMessage({
                        message: '上传文件不能超过30MB',
                        theme: 'warning'
                    })
                    return
                }
                let reader = new FileReader()
                reader.readAsText(this.fileInfo)
                reader.onload = (file) => {
                    this.formInfo.key = file.target.result
                    this.formInfo.name = this.fileInfo.name
                }
            },
            closeFile () {
                this.formInfo.name = ''
                this.formInfo.key = ''
            },
            // 添加节点
            addAreaAgentInfo (item) {
                if (!this.changeInput()) {
                    this.submitInfo()
                }
                if (!this.alreadyNodeList.length) { return }
                if (this.isSaving) {
                    return
                }
                this.isSaving = true

                let params = {}
                let appId = this.appId
                params.hosts = []
                params.op_type = 'INSTALL'
                params.node_type = this.nodeType
                params.bk_cloud_id = this.cloudId

                for (let i = 0; i < this.alreadyNodeList.length; i++) {
                    let valInfo = {
                        conn_ips: this.alreadyNodeList[i].communicationIp,
                        login_ip: this.alreadyNodeList[i].loginIp,
                        data_ip: this.alreadyNodeList[i].dataIp,
                        os_type: this.alreadyNodeList[i].osType,
                        has_cygwin: this.alreadyNodeList[i].operat === 'WindowsCygwin',
                        port: this.alreadyNodeList[i].port,
                        account: this.alreadyNodeList[i].account,
                        auth_type: this.alreadyNodeList[i].methodInfo,
                        password: this.$encrypt(this.alreadyNodeList[i].password),
                        key: this.alreadyNodeList[i].key
                    }
                    // 注册到CMDB
                    let cmdbVal = []
                    if (this.alreadyNodeList[i].toCmdbCheck.loginIp) {
                        cmdbVal.push('login_ip')
                    }
                    if (this.alreadyNodeList[i].toCmdbCheck.communicationIp) {
                        cmdbVal.push('conn_ip')
                    }
                    if (this.alreadyNodeList[i].toCmdbCheck.dataIp) {
                        cmdbVal.push('data_ip')
                    }
                    valInfo.cc_ip_types = cmdbVal.join(',')

                    if (this.alreadyNodeList[i].type !== 'AGENT') {
                        valInfo.cascade_ip = this.alreadyNodeList[i].cascadeIp
                    }
                    params.hosts.push(valInfo)
                }
                this.$store.dispatch('stall/installAgent', {appId, params}).then((res) => {
                    this.$bkMessage({
                        message: '成功开始安装任务',
                        theme: 'success'
                    })
                    this.$parent.closeAdvanced()
                    this.$emit('success', res)
                }, res => {
                    this.seeNodeInfo(this.alreadyNodeList[this.alreadyNodeList.length - 1], this.alreadyNodeList.length - 1)
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.isSaving = false
                })
            },
            addAreaOtherInfo () {
                if (!this.changeInput()) {
                    this.submitInfo()
                }
                if (!this.alreadyNodeList.length) { return }
                if (this.isSaving) { return }
                this.isSaving = true

                let params = {}
                let appId = this.appId
                params.hosts = []
                params.op_type = 'IMPORT'
                params.node_type = this.nodeType
                params.bk_cloud_id = this.cloudId

                for (let i = 0; i < this.alreadyNodeList.length; i++) {
                    let valInfo = {
                        conn_ips: this.alreadyNodeList[i].communicationIp,
                        login_ip: this.alreadyNodeList[i].loginIp,
                        data_ip: this.alreadyNodeList[i].dataIp,
                        os_type: this.alreadyNodeList[i].osType,
                        has_cygwin: this.alreadyNodeList[i].operat === 'WindowsCygwin',
                        port: this.alreadyNodeList[i].port,
                        account: this.alreadyNodeList[i].account,
                        auth_type: this.alreadyNodeList[i].methodInfo,
                        password: this.$encrypt(this.alreadyNodeList[i].password),
                        key: this.alreadyNodeList[i].key
                    }

                    // 注册到CMDB
                    let cmdbVal = []
                    if (this.alreadyNodeList[i].toCmdbCheck.loginIp) {
                        cmdbVal.push('login_ip')
                    }
                    if (this.alreadyNodeList[i].toCmdbCheck.communicationIp) {
                        cmdbVal.push('conn_ip')
                    }
                    if (this.alreadyNodeList[i].toCmdbCheck.dataIp) {
                        cmdbVal.push('data_ip')
                    }
                    valInfo.cc_ip_types = cmdbVal.join(',')

                    if (this.alreadyNodeList[i].type !== 'AGENT') {
                        valInfo.cascade_ip = this.alreadyNodeList[i].cascadeIp
                    }
                    params.hosts.push(valInfo)
                }
                this.$store.dispatch('stall/installAgent', {appId, params}).then((res) => {
                    this.$bkMessage({
                        message: '成功开始安装任务',
                        theme: 'success'
                    })
                    this.$parent.closeAdvanced()
                    this.$emit('success', res)
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.isSaving = false
                })
            },
            advancedInfo () {
                this.$parent.closeAdvanced()
                this.$emit('hideEditor')
            }
        }
    }
</script>
<style lang="scss" scoped>
    @import './advancedSet.scss'
</style>