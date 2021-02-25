<template>
    <div id="app" class="agent-app">
        <app-header @changeRouter="reloadCurPage"></app-header>
        <div v-bkloading="{isLoading: isAppLoading}" class="agent-container">
            <template v-if="isAppLoading">
                <div style="height: 500px;"></div>
            </template>
            <template v-else>
                <router-view :key="routerKey" v-if="hasProjectPermission && isRouterAlive"></router-view>
                <app-exception v-else :type="'403'" :text="$t('m.otherWord.business')" class="bk-expect"></app-exception>
            </template>
        </div>
        <app-footer></app-footer>
    </div>
</template>
<script>
    import {bus} from './utils/bus'

    export default {
        name: 'app',
        data () {
            return {
                hasProjectPermission: true,
                isRouterAlive: true,
                isAppLoading: true,
                routerKey: +new Date()
            }
        },
        computed: {
            openStatus () {
                return this.$store.state.openDoor
            }
        },
        watch: {
            '$route': function () {
                clearInterval(this.$store.state.plug.timeTaskInfo)
                clearInterval(window.setTime)
                if (this.$route.path !== '/') {
                    clearInterval(this.$store.state.stall.timeOut)
                    clearInterval(this.$store.state.stall.timeOutCheck)
                }
                if (this.$route.path !== '/task') {
                    clearInterval(this.$store.state.task.timeOutInfo)
                }
                if (this.$route.path !== '/plug') {
                    clearInterval(this.$store.state.plug.timeInfo)
                }
            }
        },
        methods: {
            reloadCurPage () {
                this.routerKey = +new Date()
            },
            initApplications () {
                this.$store.dispatch('stall/getApplications').then(res => {
                    this.isAppLoading = false
                    if (res.data.length) {
                        this.$store.state.stall.appliId = res.data[0].ApplicationID
                    }
                    if (res.data.hasOwnProperty('length') && !res.data.length && !this.openDoor) {
                        this.hasProjectPermission = false
                    } else {
                        this.hasProjectPermission = true
                    }
                }, res => {
                    if (!this.openStatus) {
                        this.isAppLoading = false
                        this.hasProjectPermission = false
                    }
                })
            },
            reload () {
                this.isRouterAlive = false
                this.$nextTick(() => (this.isRouterAlive = true))
            }
        },
        mounted () {
            this.initApplications()
            bus.$on('show-nginx-modal', () => {
                this.$store.commit('changeStatus')
            })
        }
    }
</script>

<style lang="scss">
    @import './scss/reset.scss';
    @import './scss/app.scss';
    @import './scss/bk-patch.scss';
    @import './scss/new-bk-patch.scss';
    @import './scss/animation.scss';
    .agent-container {
        min-height: 500px;
    }
    .agent-app {
        margin: 0 auto;
    }
</style>
