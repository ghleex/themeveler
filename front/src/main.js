import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import store from './store' // vuex
import VueCsrf from 'vue-csrf'
import VueSimpleAlert from "vue-simple-alert"
import axios from 'axios'

Vue.config.productionTip = false
axios.defaults.baseURL = 'http://localhost:8000'

new Vue({
  router,
  vuetify,
  store,
  VueCsrf,
  VueSimpleAlert,
  render: h => h(App)
}).$mount('#app')
