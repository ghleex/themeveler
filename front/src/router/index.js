import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Account from '../views/Account.vue'
import SearchResult from '../views/SearchResult.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', name: 'home', component: Home },
  {
    path: '/login',
    name: 'login',
    component: Account,
  },
  // { path: '/login', name: 'login', component: { template: '<div>Login</div>' }},
  // { path: '/logout', name: 'logout', component: { template: '<div>Logout</div>' }},
  { path: '/searchresult', name: 'search-result', component: SearchResult },
  // { path: '*', name: 'e404', component: { template: '<div>404 not found</div>' }},
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router