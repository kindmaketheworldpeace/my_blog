/**
 * 中文语言包
 */
export const m = {
    header: {
        title: '节点管理',
        node: '节点信息',
        manage: 'Agent安装',
        examine: '健康检查',
        schematic: 'mini手册'
    },
    search: {
        cluster: '集群',
        modules: '模块',
        changeCloud: '选择云区域',
        screen: '查询',
        placeholder: '请选择',
        searchContent: '请输入想要搜索的内容'
    },
    tabControl: {
        allArea: '所有区域',
        directArea: '直连区域',
        cloudArea: '云区域',
        cloudManag: '云区域管理',
        copyGood: '复制所选节点IP',
        copyBad: '复制异常节点IP',
        addAgent: '添加Agent',
        addProxy: '添加Proxy',
        addPagent: '添加P-Agent',
        importCmdb: '从CMDB导入',
        data: '暂无数据'
    },
    addNode: {
        nodeType: '节点类型',
        address: 'IP地址',
        innerip: '内网IP地址',
        outerip: '外网IP地址',
        please: '请输入 IP:PORT',
        port: '端口',
        account: '账号',
        verify: '校验方式',
        password: '密码验证',
        passInfo: '密码',
        passInput: '请输入密码',
        key: '密钥验证',
        upload: '上传私钥文件',
        operat: '操作系统',
        operation: '操作',
        add: '添加',
        delete: '删除',
        clickStart: '点击开始安装',
        progress: '安装中...',
        addit: '导入中...'
    },
    check: {
        address: '请填写IP地址',
        port: '请填写SSH端口',
        account: '请填写账号',
        key: '请上传私钥文件',
        agent: '添加Agent节点成功',
        proxy: '添加Proxy节点成功',
        error: '添加失败',
        legal: '端口不合法！',
        ipLegal: 'IP地址不合法！'
    },
    headTab: {
        area: '区域',
        status: '状态',
        updateTime: '更新时间',
        step: '安装步骤信息'
    },
    operateStep: {
        upgrade: '升级',
        reinstall: '重装',
        uninstall: '卸载',
        stop: '终止',
        remove: '移除',
        compile: '编辑'
    },
    addCloud: {
        deleteArea: '删除该区域前请移除该区域下的所有Proxy/Agent节点',
        newCloud: '新增云区域',
        openCloud: '确认删除当前云区域吗？',
        cloudPlace: '输入云区域名称，64个字符以内',
        deleteCloud: '删除云区域成功'
    },
    clickBtn: {
        confirm: '确定',
        configNow: '立即配置',
        cancel: '取消',
        save: '保存',
        add: '添加',
        import: '导入',
        continue: '继续',
        return: '返回',
        update: '更新',
        time: '超时时间',
        timePlace: '请输入超时时间，单位为秒'
    },
    openSlider: {
        stepInfo: '详细安装步骤',
        attention: {
            stepOne: 'Windows,Windows(Cygwin) 仅支持 Administrator/system 用户, Linux,AIX 仅支持 root 用户',
            stepTwo: '登陆 Windows 需要开通445端口, Windows(Cygwin)则通过 SSH, 445 端口均可',
            stepThree: 'APPO(运行节点管理)及Proxy 所在机器会通过上述端口登陆到 Agent 机器'
        },
        compileOpear: {
            please: '请输入IP',
            enterPort: '请输入ssh端口',
            enterAct: '请输入账号',
            reinstall: '立即重装',
            uninstall: '立即卸载',
            remove: '立即移除'
        },
        cmdb: {
            installNum: '可以安装的机器',
            continue: '点击 [继续] 忽略以上 IP 开始安装',
            return: '点击 [返回] 修改'
        }
    },
    message: {
        comfireOpera: '你是否确定该操作？',
        comfireInfo: '你是否确定该操作？',
        searchCloud: '请选择需要搜索的云区域',
        cloudName: '云区域名称不能为空！',
        cloudClash: '云区域名称与内置区域名称冲突！',
        cloudExist: '云区域已存在',
        cloudSuccess: '添加云区域成功！',
        proxy: 'Proxy节点正在编辑，确定要离开？',
        agent: 'Agent节点正在编辑，确定要离开？',
        checkInfo: '没有勾选任何信息',
        taskBegin: '任务开始执行',
        batchTask: '批量操作任务开始执行',
        task: {
            saveTask: '保存中',
            reinstallTask: '开始重装',
            uninstallTask: '开始卸载',
            removeTask: '开始移除',
            stopTask: '尝试终止',
            errorTask: '重装失败,请更正认证信息后重试',
            checkClash: '当前选中的主机中',
            doNot: '不能进行',
            runClash: '当前选中的主机中有正在执行的任务. 请取消选中这些主机后重试',
            proxyClash: '不能同时操作Proxy和P-Agent节点'
        },
        batch: {
            upgrade: '批量升级',
            reinstall: '批量重装',
            uninstall: '批量卸载',
            stop: '批量终止',
            remove: '批量移除',
            compile: '批量编辑'
        }
    },
    nginx: {
        info: {
            title: '请填写部署蓝鲸服务器中的 nginx 所在的 IP 地址及端口. Agent 的安装包将从该 nginx 上下载.',
            pointOne: '直连区域通过 nginx 内网 IP下载安装包',
            pointTwo: '非直连区域(云区域) 通过 nginx 外网 IP 下载, 并保存在 Proxy 节点上'
        },
        port: '请输入IP:PORT',
        welcome: '欢迎使用节点管理，请先配置  Nginx Server',
        configuration: '立即配置',
        save: '保存成功',
        configOk: '配置成功',
        infokey: '信息格式错误!'
    },
    otherWord: {
        all: '全部',
        fuzzy: '模糊查询',
        sureInfo: '内容格式错误, 请输入 IP:PORT',
        complete: '内网 IP 不能为空.',
        business: '没有业务，请检查 CMDB 是否正常工作',
        table: {
            connect: 'Zookeeper连接端口(zk)',
            task: '任务服务器(gse_task)',
            data: '数据服务器(gse_data)',
            text: '文件服务器(gse_btsvr)',
            agentListen: 'agent监听端口(gse_agent)',
            nginxListen: 'Nginx监听端口(nginx)',
            type: '端口类型',
            opp: '对端',
            instra: '端口说明'
        },
        figure: {
            agentInstall: 'Agent 安装流程',
            direaAgent: '直连区域 Agent 安装流程',
            appoAgent: '从 APPO 通过 SSH 登陆 Agent 机器, 下载安装脚本并执行脚本, 脚本下载安装包, 然后安装并启动 Agent',
            noAgent: '非直连 Agent 安装流程',
            appoProxy: '从 APPO 通过 SSH 登陆 Proxy 机器, 下载安装脚本, 安装好 Proxy',
            job: '从 APPO 通过 Job 作业平台发起快速脚本作业, 在 Proxy 节点上执行安装脚本(同时把要安装的 Agent 的主机列表信息传给安装脚本)',
            net: '网络访问策略',
            agentPort: '直连Agent/Proxy端：保证与蓝鲸服务端以下端口互通',
            ssh: 'APPO 到直连Agent的SSH端口(Linux/Cygwin)/SMB端口139，445(Windows)互通'
        },
        router: {
            node: '节点信息',
            manag: '安装Agent',
            healty: '健康检查',
            plug: '插件管理',
            task: '任务列表'
        }
    },
    addInfo: {
        agent: {
            condition: '服务器需要满足以下条件',
            add: '请点击添加 Agent 节点部署 Agent',
            appo: 'APPO 所在机器(在 app 运行所在机器) 必须能通过 ssh 登陆到 Agent 机器',
            zk: 'Agent 所在机器可以访问到 zk 的端口',
            opera: '支持 Linux/Windows/AIX 操作系统',
            port: 'Windows 服务器如果没有安装 Cygwin， 则需要开通SMB服务(网上邻居)的445端口',
            root: '必须使用 root/Administrator 账户'
        },
        pAgent: {
            app: '任意 Proxy 所在机器(在 app 运行所在机器) 必须能通过 ssh 登陆到 Agent 机器',
            port: 'Agent 所在机器可以访问到 Proxy 的端口'
        },
        proxy: {
            add: '先添加 Proxy 节点',
            info: '点击 +Proxy, 填入 Proxy 信息, 开始安装',
            status: 'Proxy 状态正常后， 添加 Agent (P-Agent) 节点',
            statusInfo: '点击 +Agent 按钮, 填入 Agent 信息, 开始安装',
            cloud: '云区域， 代表一组服务器, 云区域内的主机可以通过内网相互访问, Proxy 节点能与 gse server 进行通信',
            linux: 'Proxy 必须是CentOS Linux 64位操作系统， 至少有一个 IP 可与 GSE server 互通(端口请参考顶部导航中部署指引里的说明), 把该 IP 填写在外网 IP 地址栏',
            ssh: '确保 APPO 可通过 ssh 访问到 Proxy 服务器',
            nginx: '确保 Proxy 服务器能访问以 nginx 服务器',
            root: '目前仅支持 root 用户进行安装'
        }
    },
    addSomeInfo: {
        direct: '直连Agent与GSE',
        agentGse: 'Proxy与GSE',
        pagentGse: 'P-Agent与Proxy',
        source: '源地址',
        target: '目标地址',
        protocol: '端口',
        port: '协议',
        usage: '用途',
        remark: '备注',
        task: '任务服务端口',
        data: '数据上报端口',
        bt: 'BT 传输',
        btNone: 'bt传输，可不开通',
        query: '获取配置',
        random: '监听随机端口',
        ping: 'ping 告警数据上报端口',
        same: '同一子网',
        optional: '不可开通',
        andSome: '与',
        successInfo: '上传成功'
    },
    footerInfo: {
        consult: 'QQ 咨询',
        bbs: '蓝鲸论坛',
        website: '蓝鲸官网',
        web: '蓝鲸智云工作台'
    },
    otherAdd: {
        agent: '不能直接安装agent到当前业务中, 请联系该主机负责人, 在 CMDB 中将主机从原业务挪到当前业务后, 再安装 agent',
        proxy: '不能直接安装proxy到当前业务中, 请联系该主机负责人, 在 CMDB 中将主机从原业务挪到当前业务后, 再安装 proxy',
        allStop: '终止操作将会将终止当前区域下的所有任务！',
        someStop: '终止操作将终止与该节点所属任务下的其他所有节点的任务！',
        been: '已在',
        blong: '属于',
        size: '业务',
        business: '业务下安装了',
        knowIt: '知道了',
        infoSta: '当前区域中存在 P-Agent 节点, 不能卸载/移除 Proxy'
    },
    addNewInfo: {
        excelInfo: '批量导入',
        onlyMachine: '仅导入机器',
        address: 'IP地址',
        operat: '操作系统',
        port: '端口',
        account: '账号',
        password: '密码',
        upload: '点击上传或拖动文件到此处',
        reload: '执行导入',
        info: '从EXCEL文件中导入主机信息. 适用于所有各主机密码不一致的场景. 表格中的字段从左到右排列如下',
        fileError: '文件格式非法，只能上传.xlsx文件！',
        openExcel: '导出模板',
        tableName: '模板信息表',
        downloadTemplate: '下载Agent主机导入模板'
    },
    // 插件管理页面
    '精确': '精确',
    '跨页全选': '跨页全选',
    '下一步': '下一步',
    '选择主机': '选择主机',
    '选择操作类型': '选择操作类型',
    '任务详情': '任务详情',
    '不能同时对不同操作系统的主机进行操作': '不能同时对不同操作系统的主机进行操作',
    '选择操作': '选择操作',
    '插件类型': '插件类型',
    '选择插件': '选择插件',
    '选择要变更的服务': '选择要变更的服务',
    '选择要更新的插件': '选择要更新的插件',
    '选择新包': '选择新包',
    '请联系运维': '请联系运维',
    '将插件包上传到中控机的/data/src/目录并解压': '将插件包上传到中控机的/data/src/目录并解压',
    '然后执行./bkeec pack gse_plugin 更新插件信息到/data/src下': '然后执行./bkeec pack gse_plugin 更新插件信息到/data/src下',
    '值': '值',
    '文件预览': '文件预览',
    '关闭': '关闭',
    '上一步': '上一步',
    '立即执行': '立即执行',
    '进程管理': '进程管理',
    '插件更新': '插件更新',
    '插件': '插件',
    '保留原有配置文件': '保留原有配置文件',
    '仅更新文件，不重启进程': '仅更新文件，不重启进程',
    '增量更新(仅覆盖)': '增量更新(仅覆盖)',
    '覆盖更新(先删除原目录后覆盖)': '覆盖更新(先删除原目录后覆盖)',
    '请选择插件': '请选择插件',
    '请选择操作': '请选择操作',
    '请选择更新类型': '请选择更新类型',
    '请选择新包': '请选择新包',
    '返回列表': '返回列表',
    '任务类型': '任务类型',
    '目标服务': '目标服务',
    '任务ID': '任务ID',
    '安装Proxy时，需要从Nginx所在机器下载Linux、Windows、AIX所需要的agent安装包，约150 - 180 M大小': '安装Proxy时，需要从Nginx所在机器下载Linux、Windows、AIX所需要的agent安装包，约150 - 180 M大小',
    '若Proxy到Nginx之间的网络带宽较小，容易超时。可以通过增大超时时间进行设置。': '若Proxy到Nginx之间的网络带宽较小，容易超时。可以通过增大超时时间进行设置。',
    '请初始化插件信息，后台会读取中控机下的插件配置文件，如果没有初始化或者初始化失败，将无法使用插件管理相关功能': '请初始化插件信息，后台会读取中控机下的插件配置文件，如果没有初始化或者初始化失败，将无法使用插件管理相关功能',
    '最后一次配置时间': '最后一次配置时间',
    '到安装Agent页面查看': '到安装Agent页面查看',
    '成功': '成功',
    '失败': '失败',
    '执行中': '执行中',
    '已结束': '已结束',
    '终止': '终止',
    '操作者': '操作者',
    '执行日志': '执行日志',
    '当前状态': '当前状态',
    '目标机器数': '目标机器数',
    '目标进程': '目标进程',
    '配置文件': '配置文件',
    '启动时间': '启动时间',
    '云区域名称': '云区域名称',
    '云区域 ID': '云区域 ID',
    '终止成功': '终止成功',
    '云区域': '云区域',
    '时间日期': '时间日期',
    '部署逻辑': '部署逻辑',
    '蓝鲸': '蓝鲸',
    '受控主机': '受控主机',
    '请求': '请求',
    '从': '从',
    '机器下载安装脚本': '机器下载安装脚本',
    '以及安装包': '以及安装包',
    '应用从': '应用从',
    '机器': '机器',
    '登陆到目标机器': '登陆到目标机器',
    '等': '等',
    '其他服务': '其他服务',
    '运行节点管理': '运行节点管理',
    '所在的机器': '所在的机器'
}