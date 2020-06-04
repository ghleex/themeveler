import Vue from 'vue'
import App from './App'
import router from './router'
import vuetify from './plugins/vuetify'
import VueSession from 'vue-session'
import store from './store' // vuex
import VueCsrf from 'vue-csrf'
import VueSimpleAlert from "vue-simple-alert"
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'
import AOS from 'aos'
import 'aos/dist/aos.css'
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
