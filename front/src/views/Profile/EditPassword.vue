<template>
  <v-app id="editpassword">
    <Drawer class="drawer" />

    <v-content id="profile-content">
      <h2 class="content-title">비밀번호변경</h2>
      <hr>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-form>
            <v-container class="py-0">
              <v-row>
                <v-col cols="12" md="12" class="content-col">
                  <v-text-field v-model="currentPassword" label="Current Password" class="purple-input" />
                </v-col>
                <v-col cols="12" md="6" class="content-col">
                  <v-text-field v-model="newPassword" label="New Password" class="purple-input" />
                </v-col>
                <v-col cols="12" md="6" class="content-col">
                  <v-text-field v-model="confirmPassword" label="Confirm Password" class="purple-input" />
                </v-col>
                <v-col cols="4" md="6" class="text-left">
                </v-col>
                <v-col cols="8" md="6" class="text-right">
                  <v-btn color="success" class="mr-4" @click="update">수정</v-btn>
                  <v-btn color="success" class="mr-0" @click="updatecancel">취소</v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-col>

        <v-col cols="12" md="4">
          <v-card-text class="text-center">
            <h6 class="display-1 mb-1 grey--text">ad.</h6>
            <h4 class="display-2 font-weight-light mb-3 black--text"></h4>
            <p class="font-weight-light grey--text">
              개인정보 유출에 항상 주의하세요...
            </p>
            <v-btn color="success" rounded class="mr-0">Read More</v-btn>
          </v-card-text>
        </v-col>
      </v-row>
    </v-content>
  </v-app>
</template>

<script>
import axios from 'axios'
import Drawer from '@/components/Drawer.vue'
var jwt = require('jwt-simple')

export default {
  name: "editprofile",
  components: {
    Drawer
  },
  data() {
    return {
      dialog: false,
      currentPassword: "",
      newPassword: "",
      confirmPassword: ""
    }
  },
  methods: {
    update() {
      if (this.newPassword === this.confirmPassword) {
        if (this.newPassword.length > 7) {
          let data = {
            "password": this.newPassword,
            "original_password": this.currentPassword
          }
          const token = jwt.encode(data, process.env.VUE_APP_JWT_SECRET_KEY, process.env.VUE_APP_JWT_ALGORITHM)
          let form = new FormData()
          form.append("data", token)
          const requestHeader = this.$store.getters.requestHeader
          axios.put('/accounts/password/', form, requestHeader)
            .then(() => {
              this.$router.push({
                path: '/profile'
              })
            })
            .catch(err => {
              console.log(err)
            })
        }
        else {
          alert("비밀번호는 8자리이상이여야 합니다.")
        }
      }
      else {
        alert("비밀번호가 일치하지 않습니다.")
      }
    },
    updatecancel () {
      this.$router.push({
        path: '/profile'
      })
    }
  }
}
</script>

<style scoped>
  #editpassword {
    margin-top: 64px;
    background-color: rgba(245, 245, 245, 0.5);
  }

  #profile-content {
    margin-left: 256px;
    width: 80%;
  }

  @media (max-width: 600px) {
    #profile-content {
      margin-left: 56px;
      width: 80%;
    }
  }

  .content-title {
    text-align: left;
    margin-left: 20px;
    margin-top: 8px;
  }

  .content-col {
    padding-top: 6px;
    padding-bottom: 6px;
  }
</style>
