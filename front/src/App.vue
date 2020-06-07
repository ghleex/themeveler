<template>
  <v-app id="app">
    <Navbar :nickname=nickname v-on:login="login" />
    <router-view v-on:login="login"></router-view>
    <Footer />
  </v-app>
</template>

<script>
import axios from 'axios'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import Swal from 'sweetalert2'

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
          // console.log(response)
          if (response.status === 200 && response.data["token"] !== null) {
            const token = response.data.token
            this.$session.start()
            this.$session.set("jwt", token)
            this.$session.set("nickname", response.data.nickname)
            this.$session.set("anonymous", response.data.anonymous)
            this.$session.set("expire", Date.now() + 3600000)
            this.$session.set("staff", response.data.is_staff)
            this.$store.dispatch("login", token)
            this.$store.commit("setToken", token)
            this.$store.dispatch("changeNickname", response.data.nickname)
            this.$router.push('/')
          }
          else {
            alert("잘못된 정보입니다. 다시 입력해주세요.")
            this.$router.push('/login')
          }
        })
        .catch(err => {
          console.log(err)
          if (err.response.status == 404) {
            Swal.fire({
              title: "Check Email",
              text: "등록된 사용자 정보가 없습니다.",
              icon: "warning",
              timer: 3000
            })            
          } else if (err.response.status == 400) {
            Swal.fire({
              title: "Check Password",
              text: "비밀번호가 일치하지 않습니다.",
              icon: "warning",
              timer: 3000
            })
          }
        })
    }
  },
  mounted() {
    if (localStorage.getItem("vue-session-key")) {
      let stored = JSON.parse(localStorage.getItem("vue-session-key"))
      this.$store.dispatch("login", stored.jwt)
      this.$store.commit("setToken", stored.jwt)
    }
    if (this.$store.getters.isLoggedIn) {
      if (this.$store.getters.user_exptime * 1000 < Date.now()) {
        this.logout()
      }
    }
    // setInterval(() => {
    //   if (this.$session.exists("jwt")) {
    //     if (this.$session.getItem("expire") < Date.now()) {
    //       this.logout()
    //     }
    //   }
    // })
  },
  computed: {
    nickname() {
      return this.$store.state.auth.nickname
    },
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;700;900&display=swap');

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}

body::-webkit-scrollbar { 
  width: 5px; 
}

body::-webkit-scrollbar-thumb {
  background: #ffa93a; 
  border-radius: 10px;
}
</style>
