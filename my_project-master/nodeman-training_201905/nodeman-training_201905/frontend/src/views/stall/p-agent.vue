<template>
    <div class="bk-add-agent">
        <table class="bk-table has-table-hover">
            <thead>
                <tr>
                    <th style="width: 100px">{{$t('m.addNode.nodeType')}}</th>
                    <th style="width: 150px">{{$t('m.addNode.innerip')}}</th>
                    <th style="width: 150px">{{$t('m.addNode.outerip')}}</th>
                    <th style="width: 150px;">SSH {{$t('m.addNode.port')}}</th>
                    <th style="width: 150px">{{$t('m.addNode.account')}}</th>
                    <th style="width: 350px;">{{$t('m.addNode.verify')}}</th>
                    <th style="width: 130px">{{$t('m.addNode.operat')}}</th>
                    <th style="width: 160px;" class="bk-center">{{$t('m.addNode.operation')}}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(node, index) in lineAgents">
                    <td class="bk-blue">
                       Proxy 
                    </td>
                    <td>
                        <input 
                            type="text" 
                            :class="['bk-form-input', {'bk-input-checked': lineAgentsError[index].conn_ips}]"
                            :placeholder="$t('m.openSlider.compileOpear.please')" 
                            v-model="node.conn_ips"
                            @input="verifyAddAgent(node, index, 'conn_ips')">
                    </td>
                    <td>
                        <input 
                            type="text" 
                            :class="['bk-form-input', {'bk-input-checked': lineAgentsError[index].cascade_ip}]"
                            :placeholder="$t('m.openSlider.compileOpear.please')" 
                            v-model="node.cascade_ip"
                            @input="verifyAddAgent(node, index, 'cascade_ip')">
                    </td>
                    <td>
                        <bk-number :value.sync="node.port" style="width:100px;"></bk-number>
                    </td>
                    <td>
                        <input 
                            type="text" 
                            :class="['bk-form-input', {'bk-input-checked': lineAgentsError[index].account}]"
                            placeholder="root" 
                            v-model="node.account"
                            @input="verifyAddAgent(node, index, 'account')">
                    </td>
                    <td class="bk-input-select"> 
                        <div style="float: left;">
                            <bk-selector
                                style="width: 100px; margin: 0px 10px 0 0;"
                                :selected.sync="node.auth_type"
                                :list="authList">
                            </bk-selector>
                        </div>
                        <div style="float: left">
                            <input 
                                type="password" 
                                :class="['bk-form-input', {'bk-input-checked': lineAgentsError[index].password}]"
                                :placeholder="$t('m.addNode.passInput')"
                                v-show="node.auth_type === 'PASSWORD'"
                                v-model="node.password" 
                                style="width: 138px"
                                @input="verifyAddAgent(node, index, 'password')">
                            <div class="bk-form-content" v-show="node.auth_type === 'KEY'">
                                <button class="bk-button bk-default bk-input-pass" style="color: #3c96ff"><i class="bk-icon icon-plus"></i> {{$t('m.addNode.upload')}}</button>
                                <input type="file" class="bk-input-agent-file" @change="readFile(node, $event)">
                                <span class="bk-file-info">{{node.name}}</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <span style="color: #7b7d8a; cursor: default;">LINUX 64</span>
                    </td>
                    <td class="bk-center" style="text-align: center;">
                        <span @click="addLineAgent">{{$t('m.addNode.add')}}</span>
                        <span class="splice-span" @click="deleteLineAgent(index)">{{$t('m.addNode.delete')}}</span>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="bk-table-page-top">
            <div class="bk-page-info" v-show="tabName !== 'directArea'">
                <p class="bk-p-black">
                    Proxy {{$t('m.addInfo.agent.condition')}}
                </p>
                <p class="bk-p-gray">
                    1. {{$t('m.addInfo.proxy.linux')}}<br>
                    2. {{$t('m.addInfo.proxy.ssh')}}<br>
                    3. {{$t('m.addInfo.proxy.nginx')}}<br>
                    4. {{$t('m.addInfo.proxy.root')}}<br>
                </p>
            </div>
            <bk-button 
                type="primary"
                @click="addAdvancedSet">高级设置</bk-button>
            <bk-button 
                type="primary" 
                :loading="isSaving" 
                @click="addAreaAgentInfo">{{$t('m.addNode.clickStart')}}</bk-button>
        </div>
        <!-- 删除二次弹窗 -->
        <div class="bk-open-shade" v-show="agentDelete.shade"></div>
        <div class="bk-open-deletedoc" v-show="agentDelete.openAgent">
            <div class="bk-doc-content">
                <p style="text-align: justify;">
                    <span v-for="(item, index) in sameAgent">IP {{item.ip}} {{$t('m.otherAdd.been')}} {{item.business}} {{$t('m.otherAdd.business')}}Proxy</span>
                    <span>{{$t('m.otherAdd.proxy')}}</span>
                </p>
            </div>
            <div class="bk-doc-btn">
                <!-- <button class="bk-button bk-primary bk-width" @click="otherAgent">{{$t('m.clickBtn.continue')}}</button> -->
                <button class="bk-button bk-default bk-width ml10" @click="openDelete">{{$t('m.otherAdd.knowIt')}}</button>
            </div>
        </div>
    </div>
</template>
<script>
    import ajax from '../../utils/ajax'
    import bkNumber from '../../components/common/number'
    export default {
        components: {
            bkNumber
        },
        props: {
            appId: {
                type: [String, Number],
                default: ''
            },
            cloudId: {
                type: [String, Number],
                default: ''
            },
            tabName: {
                type: [String, Number],
                default: ''
            },
            length: {
                type: [String, Number],
                default: ''
            },
            addNum: {
                type: [String, Number],
                default: ''
            }
        },
        data () {
            return {
                isSaving: false,
                agentDelete: {
                    shade: false,
                    openAgent: false
                },
                index: '',
                lineAgents: [
                    {
                        conn_ips: '',
                        cascade_ip: '',
                        os_type: 'LINUX',
                        has_cygwin: false,
                        port: '',
                        account: '',
                        auth_type: 'PASSWORD',
                        password: '',
                        key: '',
                        name: ''
                    }
                ],
                lineAgentsError: [
                    {
                        conn_ips: '',
                        cascade_ip: '',
                        port: '',
                        account: '',
                        password: '',
                        key: '',
                        name: ''
                    }
                ],
                systemList: [
                    {
                        id: 'WINDOWS',
                        name: 'Windows'
                    },
                    {
                        id: 'LINUX',
                        name: 'Linux'
                    },
                    {
                        id: 'AIX',
                        name: 'AIX'
                    }
                ],
                authList: [
                    {
                        id: 'PASSWORD',
                        name: this.$t('m.addNode.password')
                    },
                    {
                        id: 'KEY',
                        name: this.$t('m.addNode.key')
                    }
                ],
                sameList: {},
                sameAgent: []
            }
        },
        methods: {
            // 高级设置
            addAdvancedSet () {
                const type = 'PROXY'
                this.$parent.showAdvancedOpen(type)
            },
            checkAgentData () {
                for (let i = 0; i < this.lineAgents.length; i++) {
                    let node = this.lineAgents[i]
                    let errors = this.lineAgentsError[i]
                    if (!node.conn_ips) {
                        this.$bkMessage({
                            message: this.$t('m.check.address') + '(' + this.$t('m.addNode.innerip') + ')',
                            theme: 'error'
                        })
                        errors.conn_ips = this.$t('m.check.address') + '(' + this.$t('m.addNode.innerip') + ')'
                        return false
                    }
                    if (!node.cascade_ip) {
                        this.$bkMessage({
                            message: this.$t('m.check.address') + '(' + this.$t('m.addNode.outerip') + ')',
                            theme: 'error'
                        })
                        errors.cascade_ip = this.$t('m.check.address') + '(' + this.$t('m.addNode.outerip') + ')'
                        return false
                    }
                    if (!node.port) {
                        this.$bkMessage({
                            message: this.$t('m.check.port'),
                            theme: 'error'
                        })
                        errors.port = this.$t('m.check.port')
                        return false
                    }
                    if (!node.account) {
                        this.$bkMessage({
                            message: this.$t('m.check.account'),
                            theme: 'error'
                        })
                        errors.account = this.$t('m.check.account')
                        return false
                    }
                    if (node.auth_type === 'PASSWORD' && !node.password) {
                        this.$bkMessage({
                            message: this.$t('m.addNode.passInput'),
                            theme: 'error'
                        })
                        errors.password = this.$t('m.addNode.passInput')
                        return false
                    }
                    if (node.auth_type === 'KEY' && !node.key) {
                        this.$bkMessage({
                            message: this.$t('m.check.key'),
                            theme: 'error'
                        })
                        errors.key = this.$t('m.check.key')
                        return false
                    }
                }
                return true
            },
            /*
            ** 添加Agent
            */
            addAreaAgentInfo (item) {
                if (this.isSaving) {
                    return
                }
                if (!this.checkAgentData()) {
                    return false
                }
                this.isSaving = true

                let params = {}
                let appId = this.appId
                params.hosts = []
                params.op_type = 'INSTALL'

                params.bk_cloud_id = this.cloudId
                params.node_type = 'PROXY'
                
                params.hosts = JSON.parse(JSON.stringify(this.lineAgents))
                for (let i = 0; i < params.hosts.length; i++) {
                    if (params.hosts[i].password !== undefined) {
                        params.hosts[i].password = this.$encrypt(params.hosts[i].password)
                    }
                }

                this.$store.dispatch('stall/installAgent', {appId, params}).then((res) => {
                    if (res.result) {
                        this.$bkMessage({
                            message: this.$t('m.check.proxy'),
                            theme: 'success'
                        })
                        this.restoreAgent()
                        this.$emit('success', res)
                        
                        setTimeout(() => {
                            this.isSaving = false
                        }, 2000)
                    }
                }, res => {
                    this.isSaving = false
                    if (res.data.messages.hasOwnProperty('other_bk_biz_id')) {
                        this.sameList = res.data.messages.other_bk_biz_id
                        this.openDelete()
                    } else {
                        this.$bkMessage({
                            message: res.data.msg || this.$t('m.check.error'),
                            theme: 'error'
                        })
                    }
                })
            },
            otherAgent () {
                if (this.isSaving) {
                    return
                }
                if (!this.checkAgentData()) {
                    return false
                }
                this.isSaving = true

                let params = {}
                let appId = this.appId
                params.hosts = []
                params.op_type = 'INSTALL'

                params.bk_cloud_id = this.cloudId
                params.node_type = 'PROXY'
                params.ignore_installed_elsewhere = 'true'
                
                params.hosts = JSON.parse(JSON.stringify(this.lineAgents))
                for (let i = 0; i < params.hosts.length; i++) {
                    if (params.hosts[i].password !== undefined) {
                        params.hosts[i].password = this.$encrypt(params.hosts[i].password)
                    }
                }
                this.$store.dispatch('stall/installAgent', {appId, params}).then((res) => {
                    if (res.result) {
                        this.agentDelete.shade = !this.agentDelete.shade
                        this.agentDelete.openAgent = !this.agentDelete.openAgent
                        this.$bkMessage({
                            message: this.$t('m.check.proxy'),
                            theme: 'success'
                        })
                        this.restoreAgent()
                        this.$emit('success', res)
                        
                        setTimeout(() => {
                            this.isSaving = false
                        }, 2000)
                    }
                }, res => {
                    this.isSaving = false
                    this.agentDelete.shade = !this.agentDelete.shade
                    this.agentDelete.openAgent = !this.agentDelete.openAgent
                    this.$bkMessage({
                        message: res.data.msg || this.$t('m.check.error'),
                        theme: 'error'
                    })
                })
            },
            openDelete (index) {
                let arrList = this.$store.state.stall.applications
                console.log(this.sameList)
                this.sameAgent = []
                for (let i = 0; i < arrList.length; i++) {
                    for (let key in this.sameList) {
                        for (let j = 0; j < this.sameList[key].length; j++) {
                            if (arrList[i].ApplicationID === this.sameList[key][j]) {
                                this.sameAgent.push({
                                    ip: key,
                                    business: arrList[i].ApplicationName
                                })
                            }
                        }
                    }
                }
                this.agentDelete.shade = !this.agentDelete.shade
                this.agentDelete.openAgent = !this.agentDelete.openAgent
                this.index = index
            },
            /*
            ** 添加Agent校验
            */
            restoreAgent () {
                this.lineAgents = [
                    {
                        conn_ips: '',
                        cascade_ip: '',
                        os_type: 'LINUX',
                        has_cygwin: false,
                        port: '',
                        account: '',
                        auth_type: 'PASSWORD',
                        password: '',
                        key: '',
                        name: ''
                    }
                ]
                this.lineAgentsError = [
                    {
                        conn_ips: '',
                        cascade_ip: '',
                        port: '',
                        account: '',
                        password: '',
                        key: '',
                        name: ''
                    }
                ]
            },
            verifyAddAgent (node, index, type) {
                let ipReg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
                switch (type) {
                    case 'conn_ips':
                        if (node.conn_ips && !ipReg.test(node.conn_ips)) {
                            this.lineAgentsError[index].conn_ips = this.$t('m.check.ipLegal')
                        } else {
                            this.lineAgentsError[index].conn_ips = ''
                        }
                        break

                    case 'cascade_ip':
                        if (node.cascade_ip && !ipReg.test(node.cascade_ip)) {
                            this.lineAgentsError[index].cascade_ip = this.$t('m.check.ipLegal')
                        } else {
                            this.lineAgentsError[index].cascade_ip = ''
                        }
                        break

                    case 'port':
                        let portReg = /^\+?[1-9][0-9]*$/
                        if (node.port && !ipReg.test(node.port)) {
                            this.lineAgentsError[index].port = this.$t('m.check.legal')
                        } else {
                            this.lineAgentsError[index].port = ''
                        }
                        break

                    case 'account':
                        if (node.account) {
                            this.lineAgentsError[index].account = ''
                        }
                        break

                    case 'password':
                        if (node.password) {
                            this.lineAgentsError[index].password = ''
                        }
                        break
                }
            },
            /*
            ** 读取文件信息
            */
            readFile (node, $event) {
                let fileInfo = $event.target.files[0]
                let reader = new FileReader()
                reader.readAsText(fileInfo)
                reader.onload = (file) => {
                    node.key = file.target.result
                    node.name = fileInfo.name
                }
            },
            /*
            ** 添加/删除一行Agent
            */
            addLineAgent () {
                let params = {
                    conn_ips: '',
                    os_type: 'LINUX',
                    has_cygwin: false,
                    port: '',
                    account: '',
                    auth_type: 'PASSWORD',
                    password: '',
                    key: '',
                    name: ''
                }
                let tipParams = {
                    conn_ips: '',
                    cascade_ip: '',
                    port: '',
                    account: '',
                    password: '',
                    key: '',
                    name: ''
                }
                
                if (this.lineAgents.length >= (2 - this.addNum)) {
                    return
                }
                this.lineAgents.push(params)
                this.lineAgentsError.push(tipParams)
            },
            deleteLineAgent (index) {
                this.index = index
                if (this.lineAgents.length > 1) {
                    this.lineAgents.splice(this.index, 1)
                    this.lineAgentsError.splice(this.index, 1)
                } else {
                    this.restoreAgent()
                    this.$emit('hideEditor')
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    /*
    ** 配置详情
    */
    .bk-stall-config {
        margin: 0 auto;
        .bk-stall-select {
            height: 107px;
            overflow: hidden;
            padding: 0px 30px;
            padding-top: 40px;
            .bk-form-item {
                float: left;
                margin-top: 0px;
                &.mr30 {
                    margin-right: 20px;
                }
                .bk-label {
                    float: left;
                    line-height: 36px;
                    font-size: 14px;
                    color: #737987;
                }
                .bk-form-content {
                    float: left;
                    input {
                        width: 222px;
                        height: 36px;
                    }
                }
            }
            .bk-form-btn {
                float: left;
                margin-left: 20px;
                margin-right: 60px;
                button {
                    width: 100px;
                    height: 36px;
                }
            }
            .bk-selcet {
                width: 300px;
                .bk-form-content {
                    input {
                        width: 327px;
                        height: 36px;
                    }
                }
            }
        }
        .bk-stall-tab {
            padding: 0px 30px; 
            .p20 {
                .bk-disabled-btn {
                    float: right;
                }
            }
        }
        .bk-tab-info {
            table {
                width: 100%;
                border: 1px solid #c3cdd7;
                border-bottom: none;
                border-top: none;
                -webkit-border-horizontal-spacing: 0px;
                -webkit-border-vertical-spacing: 0px;
                thead {
                    height: 42px;
                    tr {
                        th {
                            text-align: left;
                            border-bottom: 1px solid #c3cdd7;
                            padding: 0px 10px;
                            line-height: 42px;
                            height: 42px;
                            font-size: 12px;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            white-space: nowrap;
                            box-sizing: border-box;
                            .icon-sort {
                                font-size: 10px;
                            }
                            input {
                                margin-right: 20px;
                            }
                        }
                    }
                }
                tbody {
                    background-color: #ffffff;
                    height: 50px;
                    td {
                        line-height: 50px;
                        height: 50px!important;
                        border-bottom: 1px solid #c3cdd7;
                        font-size: 12px;
                        padding: 0px 10px;
                        img {
                            width: 16px;
                            height: 16px;
                            vertical-align: middle;
                            &.ml10 {
                                width: 20px;
                                height: 20px;
                            }
                        }
                        .bk-span-blue {
                            display: block;
                            height: 24px;
                            border-radius: 2px;
                            text-align: center;
                            line-height: 24px;
                            width: 70%;
                            background-color: #33d777;
                            color: #ffffff;
                            margin: 0 auto;
                            cursor: default;
                        }
                        .bk-span-green {
                            background-color: #33d777;
                        }
                        .bk-span-red {
                            background-color: #ff5757;
                        }
                        .bk-span-gray {
                            background-color: #dce3ea!important;
                            color: #737987!important;
                        }
                        &.bk-orgen {
                            color: #ff9600;
                        }
                        &.bk-green {
                            color: #33d777;
                        }
                        &.bk-blue {
                            color: #3e94ff;
                            padding-left: 16px;
                        }
                        span {
                            color: #3e94ff;
                            cursor: pointer;
                        }
                        .splice-span {
                            margin-left: 20px;
                        }
                    }
                }
                .bk-center {
                    text-align: center;
                    .bk-ope-color {
                        cursor: not-allowed;
                    }
                }
                .pl30 {
                    padding-left: 30px;
                    .bk-sple-class {
                        float: left;
                    }
                    .bk-div-class {
                        float: left; 
                        overflow: hidden;
                        > span {
                            margin-right: 0px!important;
                            cursor: default;
                            color: #7b7d8a;
                        }
                    }
                }
            }
            .bk-table-page {
                overflow: hidden;
                padding: 12px 30px;
                .bk-page {
                    float: right;
                }
            }
            .bk-table-page-top {
                border: 1px solid #c3cdd7;
                border-top: none;
                overflow: hidden;
                padding: 12px 30px;
                text-align: center;
                .bk-page {
                    float: right;
                }
                > span {
                    color: #3c96ff;
                    font-size: 14px;
                    cursor: pointer;
                    &.bk-ope-color {
                        cursor: not-allowed;
                    }
                }
            }
            .bk-add-agent {
                .bk-form-input {
                    width: 120px;
                }
                table {
                    tbody {
                        tr {
                            td {
                                height: 66px;
                                .bk-form-item {
                                    select {
                                        width: 70%;
                                    }
                                }
                                &.bk-input-select {
                                    .bk-form-item {
                                        width: 50%;
                                        float: left;
                                        margin-top: 0px;
                                        input {
                                            width: 90%;
                                        }
                                        select {
                                            width: 90%;
                                        }
                                    }
                                }
                                .bk-form-content {
                                    position: relative;
                                    .bk-input-agent-file {
                                        position: absolute;
                                        top: 0;
                                        left: 0;
                                        width: 138px;
                                        height: 36px;
                                        opacity: 0;
                                        cursor: pointer;
                                    }
                                    .bk-file-info {
                                        position: absolute;
                                        top: 0;
                                        right: -52px;
                                        width: 50px;
                                        color: #7b7d8a;
                                        line-height: 51px;
                                        font-size: 12px;
                                        padding: 0px 5px;
                                        overflow: hidden;
                                        text-overflow: ellipsis;
                                        white-space: nowrap;
                                        margin: 0px;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    .bk-input-checked {
        border-color: #ff6600 !important;
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
        padding: 45px 45px 40px;
        background-color: #ffffff;
        border-radius: 4px;
        .bk-doc-top {
            > p {
                font-size: 24px;
                color: #212232;
            }
        }
        .bk-doc-content {
            margin-top: 15px;
            margin-bottom: 60px;
            text-align: left;
            width: 100%;
            word-wrap: break-word;
            > p {
                font-size: 14px;
                width: 100%;
                color: #737987;
                > span {
                    display: block;
                }
            }
        }
        .bk-doc-btn {
                .bk-width {
                width: 125px;
            }
        }
    }
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
    .bk-input-pass {
        width: 138px;
    }
    .bk-page-info {
        background: #f1f5fa;
        padding: 20px 54px;
        margin: 0 auto; 
        width: 1020px;
        margin-bottom: 10px;
        text-align: left;
        > p,
        > div {
            font-size: 14px;
            color: #737987;
            line-height: 20px;
        }
        .bk-p-gray {
            color: #999;
        }
        .bk-p-black {
            color: #333;
            padding-bottom: 8px;
        }
    }
</style>