import Vue from 'vue'
import ajax from '../../utils/ajax'
import cookie from 'cookie'

export default {
    namespaced: true,
    state: {
        applications: [],
        appliId: null,
        timeOut: '',
        timeOutCheck: ''
    },
    mutations: {
        updateApplications (state, data) {
            state.applications.splice(0, state.applications.length, ...data)
        },
        changeAppliId (state, index) {
            state.appliId = index
        },
        addparams (params) {
            const CSRFToken = cookie.parse(document.cookie).bk_csrftoken
            if (CSRFToken !== undefined) {
                params.csrfmiddlewaretoken = CSRFToken
            }
        }
    },
    actions: {
        getApplications ({commit, state, dispatch}) {
            return ajax.get(`${window.site}cmdb/applications/`).then(response => {
                let res = response.data
                if (res.result) {
                    commit('updateApplications', res.data)
                }
                return res
            }, res => {
                return res
            })
        },
        installAgent ({commit, state, dispatch}, {appId, params}) {
            const CSRFToken = cookie.parse(document.cookie).bk_csrftoken
            if (CSRFToken !== undefined) {
                params.csrfmiddlewaretoken = CSRFToken
            }
            return ajax.post(`${window.site}${appId}/tasks/`, params).then(response => {
                let res = response.data
                return res
            })
        },
        checkProxy ({commit, state, dispatch}, {appId, params}) {
            const CSRFToken = cookie.parse(document.cookie).bk_csrftoken
            if (CSRFToken !== undefined) {
                params.csrfmiddlewaretoken = CSRFToken
            }
            return ajax.post(`${window.site}${appId}/hosts/proxy/check/`, params).then(response => {
                let res = response.data
                return res
            })
        },
        // 初始化数据
        getDataInfo ({commit, state, dispatch}, {appId, params}) {
            return ajax.get(`${window.site}${appId}/hosts/?${params}`).then(response => {
                let res = response.data
                return res
            })
        },
        // 查询云区域数据
        getCloudInfo ({commit, state, dispatch}, {appId}) {
            return ajax.get(`${window.site}${appId}/clouds/`).then(response => {
                let res = response.data
                return res
            })
        },
        getOneCloud ({commit, state, dispatch}, {appId, id}) {
            return ajax.get(`${window.site}${appId}/clouds/${id}/`).then(response => {
                let res = response.data
                return res
            })
        },
        // 添加云区域
        addCloudInfo ({commit, state, dispatch}, {appId, params}) {
            const CSRFToken = cookie.parse(document.cookie).bk_csrftoken
            if (CSRFToken !== undefined) {
                params.csrfmiddlewaretoken = CSRFToken
            }
            return ajax.post(`${window.site}${appId}/clouds/`, params).then(response => {
                let res = response.data
                return res
            })
        },
        // 修改云区域名称
        reviseCloud ({commit, state, dispatch}, {appId, params, id}) {
            const CSRFToken = cookie.parse(document.cookie).bk_csrftoken
            if (CSRFToken !== undefined) {
                params.csrfmiddlewaretoken = CSRFToken
            }
            return ajax.post(`${window.site}${appId}/clouds/${id}/rename/`, params).then(response => {
                let res = response.data
                return res
            })
        },
        // 删除云区域
        deleteCloud ({commit, state, dispatch}, {appId, id}) {
            return ajax.delete(`${window.site}${appId}/clouds/${id}/`).then(response => {
                let res = response.data
                return res
            })
        },
        // 设置云区域可见接口
        seeCloudEye ({commit, state, dispatch}, {appId, id, params}) {
            const CSRFToken = cookie.parse(document.cookie).bk_csrftoken
            if (CSRFToken !== undefined) {
                params.csrfmiddlewaretoken = CSRFToken
            }
            return ajax.post(`${window.site}${appId}/clouds/${id}/envisible/`, params).then(response => {
                let res = response.data
                return res
            })
        },
        closeCloudEye ({commit, state, dispatch}, {appId, id, params}) {
            const CSRFToken = cookie.parse(document.cookie).bk_csrftoken
            if (CSRFToken !== undefined) {
                params.csrfmiddlewaretoken = CSRFToken
            }
            return ajax.post(`${window.site}${appId}/clouds/${id}/disvisible/`, params).then(response => {
                let res = response.data
                return res
            })
        },
        // 获取cmdb数据
        getCmdbInfo ({commit, state, dispatch}, {appId}) {
            return ajax.get(`${window.site}cmdb/${appId}/topo/?add_hosts=1`).then(response => {
                let res = response.data
                return res
            })
        },
        // 验证cmdb选中数据
        checkCmdbInfo ({commit, state, dispatch}, {appId, params}) {
            const CSRFToken = cookie.parse(document.cookie).bk_csrftoken
            if (CSRFToken !== undefined) {
                params.csrfmiddlewaretoken = CSRFToken
            }
            return ajax.post(`${window.site}${appId}/hosts/check/`, params).then(response => {
                let res = response.data
                return res
            })
        },
        // 详细安装步骤信息
        getStepInfo ({commit, state, dispatch}, {appId, id}) {
            return ajax.get(`${window.site}${appId}/logs/${id}/`).then(response => {
                let res = response.data
                return res
            })
        },
        // 终止单个任务
        stopTask ({commit, state, dispatch}, {appId, id}) {
            return ajax.delete(`${window.site}${appId}/tasks/${id}`).then(response => {
                let res = response.data
                return res
            })
        },
        // 批量终止任务
        batchStopTask ({commit, state, dispatch}, {appId, str}) {
            return ajax.delete(`${window.site}${appId}/tasks/bulk/?jobs=${str}`).then(response => {
                let res = response.data
                return res
            })
        },
        // 查询Agent状态
        lookAgent ({commit, state, dispatch}, {appId, id}) {
            return ajax.get(`${window.site}${appId}/host_status/?host_ids=${id}`).then(response => {
                let res = response.data
                return res
            })
        },
        // 终止个数
        stopNum ({commit, state, dispatch}, {appId, id}) {
            return ajax.get(`${window.site}${appId}/tasks/running_task_count/?bk_cloud_id=${id}`).then(response => {
                let res = response.data
                return res
            })
        },
        stopSame ({commit, state, dispatch}, {appId, params}) {
            return ajax.post(`${window.site}${appId}/tasks/bulk/`, params).then(response => {
                let res = response.data
                return res
            })
        },
        getTasks ({commit, state, dispatch}, {appId, id}) {
            return ajax.get(`${window.site}${appId}/tasks/${id}`).then(response => {
                let res = response.data
                return res
            })
        }
    }
}
