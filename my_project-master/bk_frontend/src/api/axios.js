import Vue from 'vue'
import axios from 'axios'

axios.defaults.baseURL = window.siteUrl;
axios.defaults.withCredentials = false;

axios.interceptors.request.use(config => {
  let xsrfCookieName = 'csrftoken'
  config.headers['X-Requested-With'] = 'XMLHttpRequest';
  let regex = new RegExp(xsrfCookieName + '=([^;.]*).*$')
  config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
  return config
});

axios.interceptors.response.use(response => {
  if (response.status >= 400) {
      return {
          code: response.status,
          message: '请求异常，请刷新重试',
          result: false
      }
  }
  return response.data
}, error => {
  // 无权限
  if (error.response.status == 403) {
    return {
      code: 403,
      message: error.response.data.message,
      error: error,
      result: false
    }
  }
  // 未认证
  if (error.response.status == 401) {
    window.location = window.loginUrl + '&c_url=' + window.location.href
  }
  return {
    code: 500,
    message: '未知错误，请刷新重试',
    error: error,
    result: false
  }
});
Vue.prototype.$http = axios;
export const $axios = axios
