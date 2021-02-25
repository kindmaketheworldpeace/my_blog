<template>
    <div class="bk-nginx-server">
        <!-- 表单 -->
        <div class="bk-nginx-form">
            <div class="bk-nginx-info">
                <!-- 配置安装包来源 -->
                <div class="bk-package">
                    <div class="bk-package-head">
                        <span>配置安装包来源</span>
                    </div>
                    <div class="bk-package-form">
                        <form class="bk-form">
                            <div class="bk-form-item is-required">
                                <label class="bk-label">内网URL：</label>
                                <div class="bk-form-content" style="margin-left: 130px;">
                                    <input 
                                        type="text" 
                                        class="bk-form-input"
                                        style="width: 100%" 
                                        :class="{'bk-input-checked': verify.isIntra}"
                                        :placeholder="$t('m.addNode.please')" 
                                        v-model="inputIntra"
                                        @input="verifyInnerIp('inner')">
                                </div>
                            </div>
                            <div class="bk-form-item is-required">
                                <label class="bk-label">外网URL：</label>
                                <div class="bk-form-content" style="margin-left: 130px;">
                                    <input 
                                        type="text" 
                                        style="width: 100%" 
                                        class="bk-form-input" 
                                        :class="{'bk-input-checked': verify.isOuter}"
                                        placeholder="http://<IP>:<PORT>/download" 
                                        v-model="inputOuter"
                                        @input="verifyInnerIp('outer')">
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <!-- 任务安装项目 -->
                <div class="bk-package bk-ml20">
                    <div class="bk-package-head">
                        <span>任务安装项目</span>
                    </div>
                    <div class="bk-package-form">
                        <form class="bk-form">
                            <div class="bk-form-item is-required">
                                <label class="bk-label">超时时间：</label>
                                <div class="bk-form-content" style="margin-left: 130px;">
                                    <input 
                                        type="text" 
                                        class="bk-form-input"
                                        style="width: 100%" 
                                        :class="{'bk-input-checked': verify.timeOut}"
                                        placeholder="请输入超时时间" 
                                        v-model="timeOut"
                                        @input="verifyInnerIp('time')">
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <!-- GSE Server信息 -->
                <div class="bk-package bk-ml20">
                    <div class="bk-package-head">
                        <span>GSE Server信息</span>
                    </div>
                    <div class="bk-package-form">
                        <form class="bk-form">
                            <div class="bk-form-item">
                                <label class="bk-label">GSE内网IP：</label>
                                <div class="bk-form-content" style="margin-left: 130px;">
                                    <input type="text" 
                                        style="width: 100%" 
                                        class="bk-form-input"
                                        :class="{'bk-input-checked': verify.gseInner}" 
                                        v-model.trim="formInfo.gseInnerIp" 
                                        placeholder="请输入GSE内网IP"
                                        @input="verifyInnerIp('gseInner')">
                                </div>
                            </div>
                            <div class="bk-form-item">
                                <label class="bk-label">GSE外网IP：</label>
                                <div class="bk-form-content" style="margin-left: 130px;">
                                    <input type="text" 
                                        style="width: 100%" 
                                        class="bk-form-input" 
                                        :class="{'bk-input-checked': verify.gseOuter}" 
                                        v-model.trim="formInfo.gseOuterIp" 
                                        placeholder="请输入GSE外网IP"
                                        @input="verifyInnerIp('gseOuter')">
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <!-- 保存 -->
                <div class="bk-form-btn">
                    <bk-button 
                        type="primary" 
                        title="保存"
                        @click="submitUpdata">
                        保存
                    </bk-button>
                </div>
            </div>
            <div class="bk-nginx-config">
                <!-- 插件管理相关信息 -->
                <div class="bk-package bk-ml20">
                    <div class="bk-package-head">
                        <span>插件管理相关信息</span>
                    </div>
                    <div class="bk-package-form">
                        <p class="bk-package-p">最后一次配置时间：{{configTime}}</p>
                    </div>
                </div>
                <!-- 加载插件基础信息 -->
                <div class="bk-form-btn">
                    <bk-button 
                        type="primary" 
                        title="加载插件基础信息"
                        @click="updatePlugin">
                        加载插件基础信息
                    </bk-button>
                </div>
            </div>
        </div>
        <!-- 注意事项 -->
        <div class="bk-attention">
            <!-- 注意事项 -->
            <div class="bk-attention-info">
                <div class="bk-attention-head">注意事项：</div>
                <div class="bk-attention-package">
                    <p class="bk-attention-from">配置安装包来源</p>
                    <!-- <p>请填写部署蓝鲸服务器中的 nginx 所在的 IP 地址及端口. Agent 的安装包将从该 nginx 上下载. 
                        <p>1. 直连区域通过 nginx 内网 IP下载安装包 </p>
                        <p>2. 非直连区域(云区域) 通过 nginx 外网 IP 下载, 并保存在 Proxy 节点上</p>
                    </p> -->
                    <p>URL 用于在Agent/Proxy所在机器上下载对应的agent/proxy/p-agent安装包。填写不含包名的url。
                        对于社区版/企业版， URL通常是：http://&lt;NGINX_IP&gt;:&lt;NGINX_PORT&gt;/download</p>
                    <p>内网URL用于下载直连区域的包，外网URL用于下载云区域(proxy及p-agent节点)的安装包</p>
                </div>
                <div class="bk-attention-package">
                    <p class="bk-attention-from">任务安装项目</p>
                    <p>安装Proxy时，需要从Nginx所在机器下载Linux、Windows、AIX所需要的agent安装包，约150 - 180 M大小, 若Proxy到Nginx之间的网络带宽较小，容易超时。可以通过增大超时时间进行设置。</p>
                </div>
                <div class="bk-attention-package">
                    <p class="bk-attention-from">GSE Sever信息</p>
                    <p>Agent/Proxy 启动后，会尝试连接GSE, 直连区域通常内网IP, 非直连区域使用外网IP，这里的内外网不是严格意义上的私有地址或公网地址，只要能让agent连上的IP都可以。通常在NAT网络环境中需要注意使用NAT 地址。</p>
                </div>
            </div>
            <!-- 插件管理信息 -->
            <div class="bk-attention-gse">
                <div class="bk-attention-package">
                    <p class="bk-attention-from">插件管理相关信息</p>
                    <p>gse 插件在打包时(安装gse时），节点管理还未安装，因此插件的基本信息(插件描述信息，包信息，进程管理信息）还未录入到节点管理中，点击加载按钮，加载插件基础信息。通常该操作仅需要在首次使用节点管理时执行。</p>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import ajax from '../../utils/ajax'
    import cookie from 'cookie'

    export default {
        data () {
            return {
                isPluginConfiging: false,
                formInfo: {
                    innerIp: '',
                    outerIp: '',
                    timeOut: '',
                    gseInnerIp: '',
                    gseOuterIp: ''
                },
                inputIntra: '',
                inputOuter: '',
                timeOut: '',
                configTime: '',
                // 验证判定型值
                verify: {
                    isIntra: false,
                    isOuter: false,
                    timeOut: false,
                    gseInner: false,
                    gseOuter: false
                }
            }
        },
        props: {

        },
        computed: {
            appId () {
                return this.$store.state.stall.appliId
            }
        },
        mounted () {
            this.getInfo()
        },
        methods: {
            getInfo () {
                if (!this.appId) { return }
                ajax.get(window.site + 'config/kv/?key=nginx').then((res) => {
                    this.inputIntra = res.data.data.inner_url
                    this.inputOuter = res.data.data.outer_url
                }, res => {
                    this.inputIntra = ''
                    this.inputOuter = ''
                })
                ajax.get(window.site + 'config/kv/?key=timeout').then((res) => {
                    this.timeOut = res.data.data.timeout
                }, res => {
                    this.timeOut = ''
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
                ajax.get(window.site + 'config/kv/?key=gse').then((res) => {
                    this.formInfo.gseInnerIp = res.data.data.inner_ip
                    this.formInfo.gseOuterIp = res.data.data.outer_ip
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
                ajax.get(window.site + 'config/kv/?key=plugin_config').then((res) => {
                    this.configTime = res.data.data.time
                }, res => {
                    this.configTime = ''
                    if (res.data.msg !== '配置信息不存在，请先配置') {
                        this.$bkMessage({
                            message: res.data.msg,
                            theme: 'error'
                        })
                    }
                })
            },
            submitUpdata () {
                if (!(this.inputIntra)) {
                    this.$bkMessage({
                        message: this.$t('m.otherWord.complete'),
                        theme: 'error'
                    })
                    return
                } else if (this.verify.isIntra || this.verify.isOuter) {
                    this.$bkMessage({
                        message: this.$t('m.otherWord.sureInfo'),
                        theme: 'error'
                    })
                    return
                }
                this.verify.timeOut = this.timeOut < 600
                if (this.verify.timeOut) { return }
                let reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
                this.verify.gseInner = !reg.test(this.formInfo.gseInnerIp)
                this.verify.gseOuter = !reg.test(this.formInfo.gseOuterIp)
                if (this.verify.gseInner || this.verify.gseOuter) { return }
                this.updataInfo('timeout')
                this.updataInfo('nginx')
                this.updataInfo('gse')
            },
            updataInfo (keyInfo) {
                let form = {}
                form.key = keyInfo
                if (keyInfo === 'nginx') {
                    form.inner_url = this.inputIntra
                    form.outer_url = this.inputOuter
                } else if (keyInfo === 'timeout') {
                    form.timeout = this.timeOut
                } else if (keyInfo === 'gse') {
                    form.inner_ip = this.formInfo.gseInnerIp
                    form.outer_ip = this.formInfo.gseOuterIp
                }

                ajax.post(window.site + 'config/kv/', form).then((res) => {
                    this.$bkMessage({
                        message: this.$t('m.nginx.save'),
                        theme: 'success'
                    })
                    this.$parent.showChange()
                    this.$store.commit('changeDoor')
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                }).finally(() => {
                    
                })
            },
            // 加载插件基础信息
            updatePlugin () {
                if (this.isPluginConfiging) { return }
                this.isPluginConfiging = true
                ajax.post(window.site + 'global_operate/init/', {}).then((res) => {
                    this.$bkMessage({
                        message: this.$t('m.nginx.configOk'),
                        theme: 'success'
                    })
                    this.$parent.showChange()
                    this.$store.commit('changeDoor')
                }, res => {
                    if (res.code === 'INIT_FAILURE') {
                        this.$bkMessage({
                            message: res.data.msg,
                            theme: 'warning'
                        })
                    } else {
                        this.$bkMessage({
                            message: res.data.msg,
                            theme: 'error'
                        })
                    }
                }).finally(() => {
                    this.isPluginConfiging = false
                })
            },
            // 校验
            verifyInnerIp (type) {
                let reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
                if (type === 'inner') {
                    this.verify.isIntra = !this.inputIntra
                }
                if (type === 'outer') {
                    this.verify.isOuter = !this.inputOuter
                }
                if (type === 'time') {
                    this.verify.timeOut = this.timeOut < 600
                }
                if (type === 'gseInner') {
                    this.verify.gseInner = !reg.test(this.formInfo.gseInnerIp)
                }
                if (type === 'gseOuter') {
                    this.verify.gseOuter = !reg.test(this.formInfo.gseOuterIp)
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    @import '../../scss/mixins/clearfix.scss';
    @import '../../scss/mixins/scroller.scss';

    .bk-nginx-server {
        margin: 0 140px;
        height: 100%;
        overflow: auto;
        @include scroller(#fff);
        border: 1px solid #dddedf;
        background-color: #fff;
    }

    /* 表单 */
    .bk-nginx-form {
        float: left;
        width: 60%;
        height: 100%;
        border-right: 1px solid #dddedf;
    }
    .bk-nginx-info {
        height: 500px;
        padding: 27px 30px;
        border-bottom: 1px solid #dddedf;
    }
    .bk-nginx-config {
        padding: 27px 30px;
        .bk-package-p {
            font-size:14px;
            color: #737987;
            padding-left: 13px;
        }
    }
    .bk-package {
        font-size: 16px;
        color: #313b4c;
        line-height: 21px;
        .bk-package-head {
            padding-left: 13px;
            border-left: 3px solid #3c96ff;
        }
    }
    .bk-package-form {
        margin-top: 20px;
    }
    .bk-label {
        line-height: 16px;
        font-size: 14px;
        color: #737987;
        font-weight: normal;
        width: 130px;
    }
    .bk-ml20 {
        margin-top: 20px;
    }
    /* 保存 */
    .bk-form-btn {
        margin: 20px 0 0 130px;
        .bk-button {
            width: 140px;
            height: 36px;
            line-height: 36px;
            font-size: 14px;
        }
    }

    /* 注意事项 */
    .bk-attention {
        float: right;
        width: 40%;
        height: 100%;
        background-color: #fafbfd;
    }
    .bk-attention-info,
    .bk-attention-gse {
        padding: 32px 30px;
        font-size: 12px;
        color: #737987;
        line-height: 24px;
    }
    .bk-attention-info {
        height: 500px;
        border-bottom: 1px solid #dddedf;
    }
    .bk-attention-head,
    .bk-attention-from {
        font-size: 14px;
        color: #313b4c;
        line-height: 20px;
    }
    .bk-attention-from {
        font-size: 12px;
        margin-top: 8px;
    }
    .bk-attention-package {
        margin-bottom: 30px;   
    }
    .bk-input-checked {
        border-color: #ff6600 !important;
    }
</style>