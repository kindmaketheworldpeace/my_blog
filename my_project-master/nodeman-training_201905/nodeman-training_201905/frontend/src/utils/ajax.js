/**
 * @file ajax 封装
 * @author ielgnaw <wuji0223@gmail.com>
 */

import Vue from 'vue'
import axios from 'axios'
import {bus} from './bus'

const instance = axios.create({
    validateStatus: status => {
        if (status > 400) {
            console.warn(`HTTP 请求出错 status: ${status}`)
        }
        return status >= 200 && status <= 505
    },
    withCredentials: true
})

/**
 * request interceptor
 */
instance.interceptors.request.use(config => {
    // 绝对路径不走 mock
    if (!/^(https|http)?:\/\//.test(config.url)) {
        const prefix = config.url.indexOf('?') === -1 ? '?' : '&'
        config.url += prefix + 'isAjax=1'
    }
    return config
}, error => {
    return Promise.reject(error)
})

function getMsg (obj, message) {
    if (Object.prototype.toString.call(obj) === '[object Array]') {
        for (let val of obj) {
            getMsg(val, message)
        }
    } else if (Object.prototype.toString.call(obj) === '[object Object]') {
        for (let key in obj) {
            let cur = obj[key]
            getMsg(cur, message)
        }
    } else {
        message.push(obj)
    }
}

instance.interceptors.response.use(response => {
    if (!response.data || typeof response.data === 'string') {
        let msg = '后端接口数据返回为空'
        console.warn('接口异常，', 'HTTP状态码：', response.status)
        if (!response.data) {
            console.error(msg)
        }
        response.data = {
            code: response.status,
            msg: msg
        }
    } else if (response.status === 401) {
        bus.$emit('show-login-modal')
    } else if (response.status > 300) {
        console.error('HTTP请求出错，状态码为：', response.status)
        console.warn('请求信息：', response)
        let msg = response.statusText
        if (response.data && response.data.message) {
            msg = response.data.message
        }
        response.data = {
            code: response.status,
            msg: msg
        }
    } else {
        response.data.msg = ''
    }
    let messages = []
    if (response.data.messages) {
        if (Object.prototype.toString.call(response.data.messages) === '[object Object]') {
            getMsg(response.data.messages, messages)
            response.data.msg = messages.join(';')
        } else if (Object.prototype.toString.call(response.data.messages) === '[object Array]') {
            response.data.msg = response.data.messages.join(';')
        }
    } else if (response.data.message) {
        response.data.msg = response.data.message
    }
    if (response.data.code !== 'OK') {
        if (response.data.code === 'NGINX_SETTING_ERROR') {
            // this.$store.commit('changeStatus')
            bus.$emit('show-nginx-modal')
        }
        return Promise.reject(response)
    }

    return response
}, error => {
    return Promise.reject(error)
})

Vue.prototype.$http = instance

export default instance
