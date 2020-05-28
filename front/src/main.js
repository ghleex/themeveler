import Vue from 'vue'
import App from './App'
import router from './router'
import vuetify from './plugins/vuetify'
import VueSession from 'vue-session'
import store from './store' // vuex
import VueCsrf from 'vue-csrf'
import VueSimpleAlert from "vue-simple-alert"
import axios from 'axios'

Vue.config.productionTip = false
axios.defaults.baseURL = 'http://localhost:8000/api'
var options = {
  persist: true
}
Vue.use(VueSession, options)

new Vue({
  router,
  vuetify,
  store,
  VueCsrf,
  VueSimpleAlert,
  render: h => h(App)
}).$mount('#app')
