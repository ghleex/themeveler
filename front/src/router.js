import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './views/Home.vue'
import Account from './views/Account.vue'
import SearchResult from './views/SearchResult.vue'
import NoticeRead from './views/Notice/NoticeRead.vue'
import NoticeCreate from './views/Notice/NoticeCreate.vue'
import NoticeDetail from './views/Notice/NoticeDetail.vue'
import e404 from './views/e404.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/login',
    name: 'login',
    component: Account,
  },
  // {
  //   path: '/logout',
  //   name: 'logout',
  //   component: { template: '<div>Logout</div>' }
  // },
  {
    path: '/searchresult',
    name: 'search-result',
    component: SearchResult
  },
  {
    path: '/notice',
    name: 'notice-read',
    component: NoticeRead
  },
  {
    path: '/notice/create/:contentId?',
    name: 'notice-create',
    component: NoticeCreate
  },
  {
    path: '/notice/detail/:contentId',
    name: 'notice-detail',
    component: NoticeDetail
  },
  {
    path: '*',
    name: 'e404',
    component: e404
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
