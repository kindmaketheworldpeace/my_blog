import Vue from 'vue'
import ajax from '../../utils/ajax'
import cookie from 'cookie'

export default {
    namespaced: true,
    state: {
        jobId: '',
        timeInfo: '',
        timeTaskInfo: ''
    },
    mutations: {
        changeJobId (state, value) {
            state.jobId = value
        }
    },
    actions: {
        // 选择主机
        getTabList ({commit, state, dispatch}, {params, appId}) {
            return ajax.get(`${window.site}${appId}/hosts/?`, {params}).then(response => {
                let res = response.data
                return res
            })
        },
        // 操作系统类型
        getOperatType ({commit, state, dispatch}) {
            return ajax.get(`${window.site}choice/os_type`).then(response => {
                let res = response.data
                return res
            })
        },
        // 选择操作类型
        // 获取操作列表
        getOperatList ({commit, state, dispatch}) {
            return ajax.get(`${window.site}choice/op`).then(response => {
                let res = response.data
                return res
            })
        },
        // 获取插件分类
        getPlugClassifi ({commit, state, dispatch}) {
            return ajax.get(`${window.site}choice/category/`).then(response => {
                let res = response.data
                return res
            })
        },
        // 按插件分类获取插件信息
        getPlugInfo ({commit, state, dispatch}, {params}) {
            return ajax.get(`${window.site}${params}/process/`).then(response => {
                let res = response.data
                return res
            })
        },
        // 按插件获取新包
        getPackageList ({commit, state, dispatch}, {params, info}) {
            return ajax.get(`${window.site}${params}/package/?os=${info}`).then(response => {
                let res = response.data
                return res
            })
        },
        // 获取指定安装插件信息
        getRoadInfo ({commit, state, dispatch}, {params}) {
            return ajax.get(`${window.site}process_info/${params}/`).then(response => {
                let res = response.data
                return res
            })
        },
        // 分拆插件参数
        splitPlugInfo ({commit, state, dispatch}, {params, appId}) {
            const CSRFToken = cookie.parse(document.cookie).bk_csrftoken
            if (CSRFToken !== undefined) {
                params.csrfmiddlewaretoken = CSRFToken
            }
            return ajax.post(`${window.site}${appId}/tasks/split_params/`, params).then(response => {
                let res = response.data
                return res
            })
        },
        // 进程管理更新
        processManga ({commit, state, dispatch}, {params, appId}) {
            const CSRFToken = cookie.parse(document.cookie).bk_csrftoken
            if (CSRFToken !== undefined) {
                params.csrfmiddlewaretoken = CSRFToken
            }
            return ajax.post(`${window.site}${appId}/tasks/`, params).then(response => {
                let res = response.data
                return res
            })
        },
        // 通过jobId查询日志
        getTask ({commit, state, dispatch}, {params}) {
            return ajax.get(`${window.site}logs/${params}/get_steps/`).then(response => {
                let res = response.data
                return res
            })
        },
        // 获取所有的步骤
        getAllTask ({commit, state, dispatch}, {jobId, appId}) {
            return ajax.get(`${window.site}${appId}/tasks/${jobId}/get_steps/`).then(response => {
                let res = response.data
                return res
            })
        },
        // 获取任务详情
        getTaskInfo ({commit, state, dispatch}, {jobId, appId}) {
            return ajax.get(`${window.site}${appId}/tasks/${jobId}/`).then(response => {
                let res = response.data
                return res
            })
        },
        // 获取分步骤日志详情
        getStepLogs ({commit, state, dispatch}, {jobId, stepId}) {
            return ajax.get(`${window.site}logs/${jobId}/get_step_log/${stepId}/`).then(response => {
                let res = response.data
                return res
            })
        },
        // 获取软件版本列表
        getVersion ({commit, state, dispatch}, {appId, params}) {
            return ajax.get(`${window.site}${appId}/host_status/get_versions/?`, {params}).then(response => {
                let res = response.data
                return res
            })
        }
    }
}
