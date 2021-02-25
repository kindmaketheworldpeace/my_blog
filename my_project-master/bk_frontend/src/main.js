// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import store from './store'
import router from './router'
import ElementUI from 'element-ui'
import '@/api/axios'
import api from './api/api'
import '@/assets/sass/_admin.scss'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTachometerAlt, faEdit, faAngry } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import echarts from 'echarts'
import vPermission from '@/directive/permissions/permission'

Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.use(vPermission);
Vue.prototype.$echarts = echarts;
Vue.prototype.$api = api;

library.add(faTachometerAlt, faEdit, faAngry)
Vue.component('font-awesome-icon', FontAwesomeIcon)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
});
