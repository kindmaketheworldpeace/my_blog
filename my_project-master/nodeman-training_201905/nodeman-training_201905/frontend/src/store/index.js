/**
 * store 数据管理
 */

import Vue from 'vue'
import Vuex from 'vuex'

import node from './modules/node'
import stall from './modules/stall'
import health from './modules/health'
import plug from './modules/plug'
import task from './modules/task'
import ajax from '../utils/ajax'

Vue.use(Vuex)

const menuList = [
    {
        id: 1,
        name: 'm.otherWord.router.node',
        pathName: [
            'node'
        ],
        roleId: 'node'
    },
    {
        id: 2,
        name: 'm.otherWord.router.manag',
        pathName: [
            'stall'
        ],
        roleId: 'stall'
    },
    {
        id: 3,
        name: 'm.otherWord.router.plug',
        pathName: [
            'plug'
        ],
        roleId: 'plug'
    },
    {
        id: 4,
        name: 'm.otherWord.router.task',
        pathName: [
            'task'
        ],
        roleId: 'task'
    },
    {
        id: 5,
        name: 'm.otherWord.router.healty',
        pathName: [
            'health'
        ],
        roleId: 'health'
    }
]

export default new Vuex.Store({
    // 模块
    modules: {
        node,
        stall,
        health,
        plug,
        task
    },
    // 公共 store
    state: {
        // 菜单
        menuList: menuList,
        // 公共弹窗信息
        openDoor: false,
        open: false,
        // 系统当前登录用户
        user: {}
    },
    // 公共 mutations
    mutations: {
        /**
         * 更新当前用户 user
         *
         * @param {Object} state store state
         * @param {Object} user user 对象
         */
        updateUser (state, user) {
            state.user = Object.assign({}, user)
        },
        changeStatus (state) {
            state.openDoor = true
        },
        changeDoor (state) {
            state.openDoor = false
        },
        changeOpenDoor (state) {
            state.open = !state.open
        }
    },
    // 公共 actions
    actions: {
        /**
         * 获取项目里面的 rtx 人员选择器数据
         *
         * @param {Function} commit store commit mutation handler
         * @param {Object} state store state
         * @param {Function} dispatch store dispatch action handler
         * @param {string} projectId 项目 id
         *
         * @return {Promise} promise 对象
         */
        getProjectRtxList ({commit, state, dispatch}, {projectId}) {
            return ajax.get(`${window.site}/api/projects/users/?project_id=${projectId}`).then(
                response => response.data
            )
        }
    },
    // 公共 getters
    getters: {
        // use: this.$store.getters.doneTodosCount
        // doneTodosCount: (state, getters) => {
        //     console.log(111)
        //     return 222
        // }
    }
})
