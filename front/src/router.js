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
import Profile from './views/Profile/Profile.vue'
import EditPassword from './views/Profile/EditPassword.vue'
import EditProfile from './views/Profile/EditProfile.vue'
import ProfileArticle from './views/Profile/ProfileArticle.vue'
import ProfileComment from './views/Profile/ProfileComment.vue'
import ProfileTest from './views/Profile/ProfileTest.vue'
import Travel from './views/Travel/Travel.vue'
import TravelDetail from './views/Travel/TravelDetail.vue'
import TravelStart from './views/Travel/TravelStart.vue'
// import Map from './views/Map/Map.vue'
import CheckToken from './views/Social/CheckToken.vue'
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
  {
    path: '/profile',
    name: 'profile',
    component: Profile,
    // meta: {loginRequire: true}
  },
  {
    path: '/editpassword',
    name: 'editpassword',
    component: EditPassword,
    // meta: {loginRequire: true}
  },
  {
    path: '/editprofile',
    name: 'editprofile',
    component: EditProfile,
    // meta: {loginRequire: true}
  },
  {
    path: '/profile/article',
    name: 'profile-article',
    component: ProfileArticle,
    // meta: {loginRequire: true}
  },
  {
    path: '/profile/comment',
    name: 'profile-comment',
    component: ProfileComment,
    // meta: {loginRequire: true}
  },
  {
    path: '/profiletest',
    name: 'profiletest',
    component: ProfileTest
  },
  {
    path: '/travel',
    name: 'travel',
    component: Travel
  },
  {
    path: '/travel/:themeId',
    name: 'travel-detail',
    component: TravelDetail,
    props: route => ({
      themeId: Number(route.params.themeId)
    })
  },
  {
    path: '/travel/:themeId/start',
    name: 'travel-start',
    component: TravelStart,
    props: route => ({
      themeId: Number(route.params.themeId)
    })
  },
  // {
  //   path: '/map',
  //   name: 'map',
  //   component: Map
  // },




  {
    path: '/checktoken/:nickname/:token',
    name: 'checkToken',
    component: CheckToken
  },
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
