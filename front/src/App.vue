<template>
  <v-app id="app">
    <Navbar v-on:login="login" />
    <router-view v-on:login="login"></router-view>
    <Footer />
  </v-app>
</template>

<script>
import axios from 'axios'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    Footer
  },
  data() {
    return {

    }
  },
  methods: {
    logout() {
      this.$session.destroy()
      this.$store.dispatch("logout")
      this.$router.push('/')
    },
    login(loginforms) {
      axios.post('/accounts/signin/', loginforms)
        .then(response => {
          console.log(response)
          if (response.status === 200 && response.data["token"] !== null) {
            const token = response.data.token
            this.$session.start()
            this.$session.set("jwt", token)
            this.$session.set("nickname", response.data.nickname)
            this.$session.set("expire", Date.now() + 21600)
            this.$store.dispatch("login", token)
            this.$store.commit("setToken", token)
            this.$router.push('/')
          }
          else {
            alert("잘못된 정보입니다. 다시 입력해주세요.")
            this.$router.push('/login')
          }
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  mounted() {
    if (localStorage.getItem("vue-session-key")) {
      let stored = JSON.parse(localStorage.getItem("vue-session-key"))
      this.$store.dispatch("login", stored.jwt)
      this.$store.commit("setToken", stored.jwt)
    }
    // if (this.$session.exists()) {
    //   if (this.$session.get("expire") < Date.now()) {
    //     this.logout()
    //   }
    // }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>
