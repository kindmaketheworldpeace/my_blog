import api from '@/api/api'

const state = {
}

const getters = {
}

const mutations = {
}

const actions = {

  getTableUser({commit, state}, param) {
    return api.getTableUser(param)
  },
  addUser({commit, state}, param) {
    return api.addUser(param)
  },
  editUser({commit, state}, param) {
    return api.editUser(param)
  },
  deleteUser({commit, state}, param) {
    return api.deleteUser(param)
  },
  usersStatus({commit, state}, param) {
    return api.usersStatus(param)
  },
  getUserAuthority({commit, state}, param) {
    return api.getUserAuthority(param)
  },
  getAllGroup({commit, state}) {
    return api.getAllGroup()
  },
  setUserPerm({commit, state}, param) {
    return api.setUserPerm(param)
  },
  getNotInAppUser({commit, state}) {
    return api.getNotInAppUser()
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
