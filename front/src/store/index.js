import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // base_url: '',
    user_id: '',
    user_jwt: '',
    user_name: '',
    user_image: '',
    search_word: ''
  },
  mutations: {
    // urlSave (state, url) {
    //   state.base_url = url
    // },
    idSave (state, id) {
      state.user_id = id
    },
    jwtSave (state, jwt) {
      state.user_jwt = jwt
    },
    nameSave (state, name) {
      state.user_name = name
    },
    imgSave (state, img) {
      state.user_image = img
    },
    wordSave (state, word) {
      state.search_word = word
    }
  }
})
