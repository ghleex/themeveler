import jwtDecode from 'jwt-decode'

const state = {
  token: null
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

// token을 받아와서 state를 update
const mutations = {
  setToken(state, token) {
    state.token = token
  }
}

const actions =  {
  login(context, token) {
      // mutation 호출 -> commit
      context.commit('setToken', token)
  },
  logout(context) {
      context.commit('setToken', null)
  }    
}

export default {
  state,
  getters,
  mutations,
  actions
}
