import api from '@/api/api'
const state = {}
const getters = {}
const mutations = {}
const actions = {
    createScene({commit, state}, param) {
        return api.createScene(param)
    },
    getScene({commit, state}, param) {
        return api.getScene(param)
    },
    deleteScene({commit, state}, param) {
        return api.deleteScene(param)
    },
}
export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
