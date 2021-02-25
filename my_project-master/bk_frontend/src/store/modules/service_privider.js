import api from '@/api/api'

const state = {}

const getters = {}

const mutations = {}

const actions = {
    getServicePrivider({commit, state}, param) {
        return api.getServicePrivider(param)
    },
    get_bk_user({commit, state}, param) {
        return api.getBkUser(param)
    },
    modifyServicePrivider({commit, state}, param) {
        return api.modifyServicePrivider(param)
    },
    createServicePrivider({commit, state}, param) {
        return api.createServicePrivider(param)
    },
    deleteServicePrivider({commit, state}, param) {
        return api.deleteServicePrivider(param)
    }
}
export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
