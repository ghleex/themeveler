import Vue from 'vue'
import App from './App'
import router from './router'
import vuetify from './plugins/vuetify'
import VueSession from 'vue-session'
import store from './store' // vuex
import VueCsrf from 'vue-csrf'
import VueSimpleAlert from "vue-simple-alert"
import axios from 'axios'
// import io from 'socket.io-client' // socket chat

require('dotenv').config()

Vue.config.productionTip = false
axios.defaults.baseURL = process.env.VUE_APP_IP
// axios.defaults.baseURL = 'http://localhost:8000/api'
// axios.defaults.baseURL = 'https://k02b1031.p.ssafy.io:8000/api'
var options = {
  persist: true
}

// const socket = io(process.env.VUE_APP_SOCKET)
// Vue.prototype.$socket = socket

Vue.use(VueSession, options)
Vue.use(require('vue-moment'))

new Vue({
  router,
  vuetify,
  store,
  VueCsrf,
  VueSimpleAlert,
  render: h => h(App)
}).$mount('#app')
