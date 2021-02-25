import Vue from 'vue'
import ajax from '../../utils/ajax'
import cookie from 'cookie'

export default {
    namespaced: true,
    state: {
        timeOutInfo: ''
    },
    mutations: {

    },
    actions: {
        // 获取任务列表
        getTaskList ({commit, state, dispatch}, {appId, params}) {
            return ajax.get(`${window.site}${appId}/tasks/`, {params}).then(response => {
                let res = response.data
                return res
            })
        },
        // 获取任务类型
        getTaskType ({commit, state, dispatch}) {
            return ajax.get(`${window.site}choice/job_type`).then(response => {
                let res = response.data
                return res
            })
        }
    }
}
