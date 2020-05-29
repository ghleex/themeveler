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
// import Map from './views/Map/Map.vue'
import Error404 from './views/Error404.vue'
import CheckToken from './views/Social/CheckToken.vue'

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
    // meta: {loginRequired: true}
  },
  {
    path: '/editpassword',
    name: 'editpassword',
    component: EditPassword
  },
  {
    path: '/editprofile',
    name: 'editprofile',
    component: EditProfile
  },
  {
    path: '/profile/article',
    name: 'profile-article',
    component: ProfileArticle
  },
  {
    path: '/profile/comment',
    name: 'profile-comment',
    component: ProfileComment
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
    path: '/travel/:travelId',
    name: 'travel-detail',
    component: TravelDetail
  },
  // {
  //   path: '/map',
  //   name: 'map',
  //   component: Map
  // },




  {
    path: '*',
    name: 'error404',
    component: Error404
  },
  {
    path: '/checktoken/:nickname/:token',
    name: 'checkToken',
    component: CheckToken
  },
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
