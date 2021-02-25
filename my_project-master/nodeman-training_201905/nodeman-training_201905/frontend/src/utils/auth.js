/**
 * 登录
 */

import _ from 'lodash'
import {bus} from './bus'
import ajax from './ajax'

const ANONYMOUS_USER = {
    id: null,
    isAuthenticated: false,
    username: 'anonymous',
    avatarUrl: null,
    chineseName: 'anonymous',
    phone: null,
    email: null
}

let currentUser = {
    avatar_url: '',
    bkpaas_user_id: '',
    chinese_name: '',
    username: ''
}

/**
 * 转换 user 对象，注意 camelCase
 *
 * @param {Object} data 待转换的对象
 *
 * @return {Object} 结果
 */
const transformUserData = data => {
    const user = {}
    Object.keys(data).forEach((key, index) => {
        const value = data[key]
        key = _.camelCase(key)
        user[key] = value
    })
    return user
}

export default {
    HTTP_STATUS_UNAUTHORIZED: 401,
    getCurrentUser () {
        return currentUser
    },
    getAnonymousUser () {
        return {...ANONYMOUS_USER}
    },
    redirectToLogin () {
        window.location = LOGIN_SERVICE_URL + '/?c_url=' + window.location.href
    },
    requestCurrentUser () {
        let promise = null
        if (currentUser.bkpaas_user_id) {
            promise = new Promise((resolve, reject) => {
                const user = transformUserData(currentUser)
                if (user.code && user.code === 'Unauthorized') {
                    user.isAuthenticated = false
                } else {
                    user.isAuthenticated = true
                }
                resolve(user)
            })
        } else {
            // Request user endpoint and set user info to currentUser
            const endpoint = window.site + '/api/user/'
            // const req = request.get(endpoint).withCredentials()
            const req = ajax.get(endpoint, {withCredentials: true})
            promise = new Promise((resolve, reject) => {
                req.then(resp => {
                    const user = transformUserData(resp.data.data)
                    if (user.code && user.code === 'Unauthorized') {
                        user.isAuthenticated = false
                    } else {
                        user.isAuthenticated = true
                    }
                    // 存储当前用户信息(全局)
                    currentUser = resp.data.data
                    resolve(user)
                }, err => {
                    // When access to domain through smart proxy, it will redirect request to login page
                    // and thus trigger a cross-domain error
                    if (err.status === this.HTTP_STATUS_UNAUTHORIZED || err.crossDomain) {
                        resolve({...ANONYMOUS_USER})
                    } else {
                        reject(err)
                    }
                })
            })
        }

        return promise
    }
}
