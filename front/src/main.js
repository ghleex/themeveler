import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import VueCsrf from 'vue-csrf'
import VueSimpleAlert from "vue-simple-alert"

Vue.config.productionTip = false

new Vue({
  router,
  vuetify,
  VueCsrf,
  VueSimpleAlert,
  render: h => h(App)
}).$mount('#app')
