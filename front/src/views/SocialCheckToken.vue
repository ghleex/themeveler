<template>
  <div>

  </div>
</template>

<script>
  import axios from 'axios'
  import jwtDecode from 'jwt-decode'

  export default {
    beforeRouteEnter(to, from, next) {
      // console.log(from)
      if (from.name) {
        alert("잘못된 접근입니다.")
      }
      next((vm) => {
          vm.from = from;
      });
    },
    mounted() {
      const token = this.$route.params.token
      const jwtData = jwtDecode(this.$route.params.jwtData)
      var form = new FormData()
      form.append("token", token)
      axios.post("/accounts/token/verify/", form)
        .then(() => {
          this.$session.start()
          this.$session.set("jwt", token)
          this.$session.set("nickname", jwtData.nickname)
          this.$session.set("anonymous", jwtData.anonymous)
          this.$session.set("staff", false)
          this.$session.set("social", true)
          this.$store.dispatch("login", token)
          this.$store.commit("setToken", token)
          this.$store.dispatch("changeNickname", jwtData.nickname)
          this.$store.dispatch("changeAnonymous", jwtData.anonymous)
          this.$router.push({ name: "home" })
        })
        .catch(error => {
          console.log(error)
          alert("잘못된 접근입니다.")
          this.$router.push({ name: "home" })
        }) 
    }
  }
</script>

<style lang="scss" scoped>

</style>