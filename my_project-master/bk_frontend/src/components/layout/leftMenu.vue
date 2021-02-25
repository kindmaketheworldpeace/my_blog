<template>
    <div class="menu" :style="isCollapse ? 'width: auto' : 'width: 230px'">
        <el-menu
                router
                :default-active="currentMenu"
                background-color="rgb(42, 47, 55)"
                text-color="#fff"
                :unique-opened="only"
                :collapse="isCollapse">
            <template v-for="(item, index) in routerMenuList">
                <el-submenu :index="index + ''" :key="index" v-if="item.children.length > 0 && item.is_menu">
                    <template slot="title">
                        <font-awesome-icon :icon="item.icon"></font-awesome-icon>
                        <span class="menu-name">{{item.display_name}}</span>
                    </template>
                    <el-menu-item v-for="(itemChild, indexChild) in item.children" :index="itemChild.path"
                                  :key="indexChild">
                        <span class="menu-sub-name" v-if="itemChild.is_menu">{{itemChild.display_name}}</span>
                    </el-menu-item>
                </el-submenu>
                <el-menu-item :index="item.path" :key="item.path" v-else-if="item.children == 0 && item.is_menu">
                    <font-awesome-icon :icon="item.icon"></font-awesome-icon>
                    <span class="menu-name">{{item.display_name}}</span>
                </el-menu-item>
            </template>
        </el-menu>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex'

    export default {
        data() {
            return {
                only: true,
                currentMenu: '/home',
                menusList: [
                    {children: []}
                ]
            }
        },
        created() {
            this.$root.$on('change', (val) => {
                this.isCollapse = val
            })
            this.getUrl()
        },
        computed: {
            ...mapGetters('leftmenu', ['routerMenuList']),
            ...mapGetters('main', ['isCollapse'])
        },
        methods: {
            getUrl() {
                /*
                * 刷新当前页面左侧对应菜单高亮
                * @param    currentUrl       当前url
                * @param    currentMenu      当前菜单
                */
                let self = this
                let currentUrl = window.location.href;
                self.currentMenu = self.$route.meta.currentMenu
            },
            getPath() {
                /*
                * 点击浏览器前进后退按钮高亮显示同步
                */
                let self = this
                self.currentMenu = self.$route.meta.currentMenu
            },
        },
        watch: {
            /*
            * 监听路由，当路由变化时，改变默认显示高亮的值
            */
            '$route': 'getPath'
        }
    }
</script>
