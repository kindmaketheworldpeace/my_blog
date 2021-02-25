import api from '@/api/api'

const state = {
}

const getters = {
}

const mutations = {
}

const actions = {
  getGroups({commit, state}, param) {
    return api.getGroups(param)
  },
  editGroups({commit, state}, param) {
    return api.editGroups(param)
  },
  addGroups({commit, state}, param) {
    return api.addGroups(param)
  },
  getAllUser({commit, state}, param) {
    return api.getAllUser()
  },
  deleteGroups({commit, state}, param) {
    return api.deleteGroups(param)
  },
  groupsStatus({commit, state}, param) {
    return api.groupsStatus(param)
  },
  getAuthority({commit, state}, param) {
    return api.getAuthority(param)
  },
  getPermsTree({commit, state}, param) {
    return api.getPermsTree(param)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
