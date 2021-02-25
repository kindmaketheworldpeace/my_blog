<template>
    <div class="header">
        <div class="header-left">
            <img src="../../assets/img/logo_new.png">
            <span class="header-left-word">蓝鲸开发框架</span>
            <div class="header-left-icon" @change="changeShow">
                <el-radio-group :value="isCollapse">
                    <el-radio-button :label="true" v-show="!isCollapse">
                        <i class="el-icon-s-fold"></i>
                    </el-radio-button>
                    <el-radio-button :label="false" v-show="isCollapse">
                        <i class="el-icon-s-unfold"></i>
                    </el-radio-button>
                </el-radio-group>
            </div>
        </div>
        <div class="header-right">
            <img class="photo" src="../../assets/img/photo.jpg">
            <span class="header-right-name">{{username}}</span>
            <a :href="logout_url" class="login-out el-icon-time"></a>
        </div>
    </div>
</template>

<script>
    import { mapGetters, mapMutations } from 'vuex'

    export default {
        name: 'cw-header',
        data() {
            return {
                username: window.userName,
                logout_url: ''
            }
        },
        computed: {
            ...mapGetters('main', ['isCollapse'])
        },
        methods: {
            changeShow() {
                let isCollapse = !this.isCollapse
                this.$store.commit('main/setIsCollapse', isCollapse)
                // 保证菜单完全收缩或者拉伸后，再给window添加resize事件
                setTimeout(() => {
                  let resizeEvent = new Event('resize')
                  window.dispatchEvent(resizeEvent)
                }, 100)
            }
        },
    }
</script>
