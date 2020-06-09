import jwtDecode from 'jwt-decode'
import getter from './getter.js'

const state = {
  token: getter.getToken(),
  nickname: getter.getNickname(),
  anonymous: getter.getAnonymous()
}

// token을 받아와서 state를 update
const mutations = {
  setToken(state, token) {
    state.token = token
  },
  setNickname(state, nickname) {
    state.nickname = nickname
  },
  setAnonymous(state, anonymous) {
    state.anonymous = anonymous
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
  },
  changeAnonymous(context, anonymous) {
    context.commit('setAnonymous', anonymous)
  }
}

const getters = {
  isLoggedIn: state => state.token ? true : false,
  requestHeader(state) {
    if (state.token == null || state.token == undefined) {
      return {
        headers: {
          Authorization: ''
        }
      }
    }
    return {
      headers: {
        Authorization: `JWT ${state.token}`
      }
    }
  },
  user_id(state) {
    return jwtDecode(state.token).user_id
  },
  username(state) {
    return jwtDecode(state.token).username
  },
  user_exptime(state) {
    return jwtDecode(state.token).exp
  }
}

export default {
  state,
  getters,
  mutations,
  actions
}
