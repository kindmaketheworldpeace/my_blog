import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'
import {mapGetters} from 'vuex'

const User = () => import('@/pages/user_page/user')
const Group = () => import('@/pages/group_page/Group')
const Permission = () => import('@/pages/group_page/Permission')
const Home = () => import('@/pages/home_page/Home')
const NormalChange = () => import('@/pages/normal_change_page/NormalChange')
const SelfChange = () => import('@/pages/self_change_page/SelfChange')
const CreateScene = () => import('@/pages/create_scene_page/CreateScene')
const CreateRule = () => import('@/pages/create_rule_page/CreateRule')
const ServicePrivider = () => import('@/pages/service_privider_page/ServicePrivider')
const OprateLog = () => import('@/pages/oprate_log_page/OprateLog')
const editChange = () => import('@/pages/normal_change_page/editChange')
const SceneControl = () => import('@/pages/scene_control_page/SceneControl')
const RuleControl = () => import('@/pages/rule_control_page/RuleControl')
Vue.use(Router);

let routerVue = new Vue({
    store,
    methods: {
        // 当前用户是否有路由权限
        async isRouterNameAuthority(routerName) {
            // 当前用户能访问的路由列表是否已获取,如果没有获取,则请求获取路由权限接口
            if (!this.isGetUserPerm) {
                await this.$store.dispatch('leftmenu/getCurrentPermission')
            }
            // 判断当前用户能访问的路由
            // 第一步，首先判断用户是否为管理员
            if (this.isAdmin) {
                return true
            }
            let authorityRes = false
            for (let i = 0; i < this.routerList; i++) {
                if (this.routerList[i].name == routerName) {
                    authorityRes = true
                    break
                }
            }
            return authorityRes
        }
    },
    computed: {
        ...mapGetters('leftmenu', ['isAdmin', 'isGetUserPerm', 'routerList'])
    }
})

let router = new Router({
    routes: [
        {
            path: '/',
            redirect: 'home'
        },

        {
            path: '/403',
            component: resolve => require(['@/pages/403'], resolve)
        },
        {
            path: '/404',
            component: resolve => require(['@/pages/404'], resolve)
        },
        {
            path: '/home',
            name: 'home',
            component: Home,
            meta: {
                bread: [
                    {displayName: '首页管理', path: ''},
                ],
                currentMenu: '/home'
            }
        },

        {
            path: '/user',
            name: 'user',
            component: User,
            meta: {
                bread: [
                    {displayName: '权限管理', path: ''},
                    {displayName: '用户管理', path: '/user'},
                ],
                currentMenu: '/user'
            }
        },
        {
            path: '/group',
            name: 'group',
            component: Group,
            meta: {
                bread: [
                    {displayName: '权限管理', path: ''},
                    {displayName: '角色管理', path: '/group'},
                ],
                currentMenu: '/group'
            },
        },
        {
            path: '/normal_change',
            name: 'normal_change',
            component: NormalChange,
            meta: {
                bread: [
                    {displayName: '变更管理', path: ''},
                    {displayName: '常规变更', path: '/normal_change'},
                ],
                currentMenu: '/normal_change'
            },
        }, {
            path: '/edit_change',
            name: 'edit_change',
            component: editChange,
            meta: {
                bread: [
                    {displayName: '变更管理', path: ''},
                     {displayName: '任务管理', path: ''},
                    {displayName: '新建变更', path: '/edit_change'},
                ],
                currentMenu: '/edit_change'
            },
        },
         {
            path: '/self_change',
            name: 'self_change',
            component: SelfChange,
            meta: {
                bread: [
                    {displayName: '变更管理', path: ''},
                    {displayName: '自定义变更', path: '/self_change'},
                ],
                currentMenu: '/self_change'
            },
        },
         {
            path: '/create_scene',
            name: 'create_scene',
            component: CreateScene,
            meta: {
                bread: [
                    {displayName: '变更管理', path: ''},
                    {displayName: '新建场景', path: '/create_scene'},
                ],
                currentMenu: '/create_scene'
            },
        },
         {
            path: '/scene_control',
            name: 'scene_control',
            component: SceneControl,
            meta: {
                bread: [
                    {displayName: '变更管理', path: ''},
                    {displayName: '场景管理', path: '/scene_control'},
                ],
                currentMenu: '/scene_control'
            },
        },
        {
            path: '/rule_control',
            name: 'rule_control',
            component: RuleControl,
            meta: {
                bread: [
                    {displayName: '复核管理', path: ''},
                    {displayName: '规则管理', path: '/rule_control'},
                ],
                currentMenu: '/rule_control'
            },
        },
        {
            path: '/create_rule',
            name: 'create_rule',
            component: CreateRule,
            meta: {
                bread: [
                    {displayName: '复核管理', path: ''},
                    {displayName: '新建规则', path: '/create_rule'},
                ],
                currentMenu: '/create_rule'
            },
        },
        {
            path: '/service_privider',
            name: 'service_privider',
            component: ServicePrivider,
            meta: {
                bread: [
                    {displayName: '系统管理', path: ''},
                    {displayName: '标段管理', path: '/service_privider'},
                ],
                currentMenu: '/service_privider'
            }
        },
        {
            path: '/oprate_log',
            name: 'oprate_log',
            component: OprateLog,
            meta: {
                bread: [
                    {displayName: '系统管理', path: ''},
                    {displayName: '标段管理', path: '/oprate_log'},
                ],
                currentMenu: '/oprate_log'
            }
        },
        {
            path: '/permission/:group_id',
            name: 'permission',
            component: Permission,
            meta: {
                bread: [
                    {displayName: '系统管理', path: ''},
                    {displayName: '角色管理', path: '/group'},
                    {displayName: '功能权限', path: ''},
                ],
                currentMenu: '/group'
            }
        },
        {
            path: '/permission/:group_id',
            name: 'permission',
            component: Permission,
            meta: {
                bread: [
                    {displayName: '系统管理', path: ''},
                    {displayName: '角色管理', path: '/group'},
                    {displayName: '功能权限', path: ''},
                ],
                currentMenu: '/group'
            }
        },
    ]
});

router.beforeEach(async (to, from, next) => {
    if (to.matched.length === 0) {
        from.name ? next({name: from.name}) : next('/404');
    } else {
        let authorityResult = await routerVue.isRouterNameAuthority(to.name)
        if (authorityResult || ['/403', '/404'].indexOf(to.path != -1)) {
            next();
        } else {
            next('/403');
        }
    }
});
export default router
