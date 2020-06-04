import jwtDecode from 'jwt-decode'
import getter from './getter.js'

const state = {
  token: getter.getToken(),
  nickname: getter.getNickname()
}

// token을 받아와서 state를 update
const mutations = {
  setToken(state, token) {
    state.token = token
  },
  setNickname(staet, nickname) {
    staet.nickname = nickname
  }
}

const actions =  {
  login(context, token) {
    // mutation 호출 -> commit
    context.commit('setToken', token)
  },
  logout(context) {
    context.commit('setToken', null)
  },
  changeNickname(context, nickname) {
    context.commit('setNickname', nickname)
  }
}

const getters = {
  isLoggedIn: state => state.token ? true : false,
  requestHeader(state) {
    return {
      headers: {
        Authorization: `JWT ${state.token}`
      }
    }
  },
  user_id(state) {
    return jwtDecode(state.token).user_id
  }
}

export default {
  state,
  getters,
  mutations,
  actions
}
