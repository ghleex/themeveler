import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './views/Home.vue'
import Account from './views/Account.vue'
import SearchResult from './views/SearchResult.vue'
import NoticeRead from './views/Notice/NoticeRead.vue'
import NoticeCreate from './views/Notice/NoticeCreate.vue'
import NoticeDetail from './views/Notice/NoticeDetail.vue'
import ServiceRead from './views/ServiceCenter/ServiceRead.vue'
import ServiceCreate from './views/ServiceCenter/ServiceCreate.vue'
import ServiceDetail from './views/ServiceCenter/ServiceDetail.vue'
// import CustomerCenterRead from './views/CustomerCenter/CustomerCenterRead.vue'
// import CustomerCenterCreate from './views/CustomerCenter/CustomerCenterCreate.vue'
// import CustomerCenterDetail from './views/CustomerCenter/CustomerCenterDetail.vue'
// import Map from './views/Map/Map.vue'
import Error404 from './views/Error404.vue'

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
    path: '/notice/create/:noticeId?',
    name: 'notice-create',
    component: NoticeCreate
  },
  {
    path: '/notice/detail/:noticeId',
    name: 'notice-detail',
    component: NoticeDetail
  },
  {
    path: '/service',
    name: 'service-read',
    component: ServiceRead
  },
  {
    path: '/service/create/:serviceId?',
    name: 'service-create',
    component: ServiceCreate
  },
  {
    path: '/service/detail/:serviceId',
    name: 'service-detail',
    component: ServiceDetail
  },
  // {
  //   path: '/customercenter',
  //   name: 'customercenter-read',
  //   component: CustomerCenterRead
  // },
  // {
  //   path: '/customercenter/create/:customercenterId?',
  //   name: 'customercenter-create',
  //   component: CustomerCenterCreate
  // },
  // {
  //   path: '/customercenter/detail/:customercenterId',
  //   name: 'customercenter-detail',
  //   component: CustomerCenterDetail
  // },
  // {
  //   path: '/map',
  //   name: 'map',
  //   component: Map
  // },



  
  {
    path: '*',
    name: 'error404',
    component: Error404
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
