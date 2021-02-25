/**
 * @desc router 配置
 * @example 路由组件名统一首字母大写
 */

import Vue from 'vue'
import Router from 'vue-router'
import Node from '../views/node'
import stall from '../views/stall'
import health from '../views/health'
import plug from '../views/plug'
import task from '../views/task'

Vue.use(Router)

// from webpack 2.4
// https://github.com/webpack/webpack/releases/tag/v2.4.0

const routes = [
    {
        path: '/',
        name: 'stall',
        component: stall
    },
    {
        path: '/node',
        name: 'node',
        component: Node
    },
    // {
    //     path: '/stall',
    //     name: 'stall',
    //     component: stall
    // },
    {
        path: '/health',
        name: 'health',
        component: health
    },
    {
        path: '/plug',
        name: 'plug',
        component: plug
    },
    {
        path: '/task',
        name: 'task',
        component: task
    }
]

const router = new Router({
    mode: 'hash',
    routes: routes
})

router.beforeEach((to, from, next) => {
    next()
})

router.afterEach(route => {
})

export default router
