import Vue from 'vue'
import App from './App'
import router from './router'
import vuetify from './plugins/vuetify'
import VueSession from 'vue-session'
import store from './store' // vuex
import VueCsrf from 'vue-csrf'
import VueSimpleAlert from "vue-simple-alert"
import axios from 'axios'
import AOS from 'aos' // fadeIn 이외에 scoll 효과
import 'aos/dist/aos.css'
import 'bootstrap/dist/css/bootstrap.min.css' // bootstrap
// import io from 'socket.io-client' // socket chat

require('dotenv').config()

Vue.config.productionTip = false
axios.defaults.baseURL = process.env.VUE_APP_IP
// URL = 'http://localhost:8000/api'
// URL = 'https://k02b1031.p.ssafy.io:8000/api'
var options = {
  persist: true
}
// const socket = io(process.env.VUE_APP_SOCKET)
// Vue.prototype.$socket = socket

// fontawsome security policy 참고 (해당 config로 인한 i => svg 태그로 자동 변환, 이에 따른 태그 적용은 index.html head에 유효)
import fontawesome from '@fortawesome/fontawesome-free'
fontawesome.config = {
  autoAddCss: false
}

Vue.use(VueSession, options)
Vue.use(require('vue-moment'))
AOS.init()

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isLoggedIn) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

new Vue({
  router,
  vuetify,
  store,
  VueCsrf,
  VueSimpleAlert,
  render: h => h(App)
}).$mount('#app')
