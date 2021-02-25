import api from '@/api/api'

const state = {
}

const getters = {
}

const mutations = {
}

const actions = {
  getTaskState({commit, state}) {
    return api.getTaskState()
  },
  getServerSelect({commit, state}) {
    return api.getServerSelect()
  },
  getServerPerformance({commit, state}, param) {
    return api.getServerPerformance(param)
  },
  getBizServer({commit, state}) {
    return api.getBizServer()
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
