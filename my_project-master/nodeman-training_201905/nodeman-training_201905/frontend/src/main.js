import Vue from 'vue'
import Vuex from 'vuex'
import cookie from 'cookie'
import bkMagic from '@tencent/bk-magic'

// view components
import App from './App'
import {bus} from './utils/bus'
import auth from './utils/auth'
import Header from './views/header.vue'
import Footer from './views/footer.vue'

// components
import router from './router'
import Exception from './components/common/exception'
import Img403 from './images/403.png'

import ajax from './utils/ajax'
import store from './store'
import JsEncrypt from 'jsencrypt'
import $ from 'jquery'
import VueI18n from 'vue-i18n'

// 引用导入导出excel
import Blob from './vendor/Blob.js'
import Export2Excel from './vendor/Export2Excel.js'

Vue.prototype.$encrypt = (str) => {
    var encrypt = new JsEncrypt()
    encrypt.setPublicKey(window.pubkey)
    return encrypt.encrypt(str)
}

Vue.use(bkMagic)

Vue.component('app-header', Header)
Vue.component('app-footer', Footer)
Vue.component('app-exception', Exception)

// 跨域处理
const injectCSRFTokenToHeaders = () => {
    ajax.defaults.headers.common['X-REQUESTED-WITH'] = 'XMLHttpRequest'
    const CSRFToken = cookie.parse(document.cookie).bk_csrftoken
    if (CSRFToken !== undefined) {
        ajax.defaults.headers.common['X-CSRFToken'] = CSRFToken
    } else {
        console.warn('Can not find backend_csrftoken in document.cookie')
    }
}

// 国际化
Vue.use(VueI18n)
// Vue.use(VueI18n, {
//     i18n: function (path, options) {
//         let value = i18n.t(path, options)
//         if (value !== null && value !== undefined) {
//             return value
//         }
//         return ''
//     }
// })

let localeCookie = cookie.parse(document.cookie).blueking_language ? cookie.parse(document.cookie).blueking_language : 'zh-cn'
console.log(localeCookie)
const i18n = new VueI18n({
    // 语言标识
    locale: localeCookie,
    fallbackLocale: 'zh-cn',
    // this.$i18n.locale 通过切换locale的值来实现语言切换
    messages: {
        // 中文语言包
        'zh-cn': require('./languager/lang/zh'),
        // 英文语言包
        'en': require('./languager/lang/en')
    }
})

ajax.interceptors.response.use(response => {
    return response
}, error => {
    // 登录控制
    if (error.status === 401) {
        // bus.$emit('show-login-modal')
        window.location.href = window.siteHome
    }
    // 权限控制
    if (error.status === 403) {
        bus.$emit('api-error:user-permission-denied')
    }
    return Promise.reject(error)
})

// 如果是本地开发，前端验证登录状态
if (NODE_ENV === 'development') {
    let bkCookies = cookie.parse(document.cookie)
    bkCookies.bk_uid = '123'
    if (bkCookies.bk_uid) {
        let app = new Vue({
            el: '#app',
            i18n,
            router,
            store,
            template: '<App/>',
            components: {
                App
            },
            created () {
                injectCSRFTokenToHeaders()
            }
        })
    } else {
        // auth.redirectToLogin()
    }
} else {
    let app = new Vue({
        el: '#app',
        i18n,
        router,
        store,
        template: '<App/>',
        components: {
            App
        },
        created () {
            injectCSRFTokenToHeaders()
        }
    })
}
