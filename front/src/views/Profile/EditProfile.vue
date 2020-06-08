<template>
  <v-app id="editprofile">
    <Drawer class="drawer" />

    <v-content id="profile-content">
      <h2 class="content-title">
        <v-icon style="font-size: 40px; color: black;">mdi-account-edit</v-icon>회원정보수정
      </h2>
      <hr>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-form>
            <v-container class="py-0">
              <v-row>
                <!-- <v-col cols="12" class="content-col">
                  <v-file-input label="Profile Image" class="purple-input" type="file" />
                </v-col> -->
                <v-col cols="12" class="content-col">
                  <v-text-field v-model="email" label="Email (ID)" class="purple-input" disabled />
                </v-col>
                <v-col cols="12" class="content-col">
                  <v-text-field v-model="nickname" label="Nickname" class="purple-input" />
                </v-col>
                <v-col cols="4" md="6" class="text-left">
                  <v-btn color="red" class="mr-0 text-white" @click="userdelete">회원탈퇴</v-btn>
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
            <h6 class="display-1 mb-1 grey--text">caution.</h6>
            <h4 class="display-2 font-weight-light mb-3 black--text"></h4>
            <p class="font-weight-light grey--text">
              개인정보 유출에 항상 주의하세요..
            </p>
          </v-card-text>
        </v-col>
      </v-row>
    </v-content>
  </v-app>
</template>

<script>
  import axios from 'axios'
  import Drawer from '@/components/Drawer.vue'

  export default {
    name: "editprofile",
    components: {
      Drawer
    },
    data() {
      return {
        dialog: false,
        email: "",
        nickname: ""
      }
    },
    methods: {
      userdelete() {
        var result = confirm("정말로 회원을 탈퇴하시겠습니까?")
        if (result) {
          axios.delete('/accounts/usermgmt/', this.$store.getters.requestHeader)
            .then(() => {
              if (this.$session.exists()) {
                this.$session.destroy()
              }
              this.$store.dispatch("logout")
              this.$router.push({
                path: '/'
              })
            })
            .catch(err => {
              console.log(err)
            })
        }
        else {
          this.$router.push({
            path: '/profiles'
          })
        }
      },
      update() {
        let form = new FormData()
        form.append("nickname", this.nickname)
        axios.put('/accounts/usermgmt/', form, this.$store.getters.requestHeader)
          .then(() => {
            alert("회원 정보가 성공적으로 변경되었습니다.")
            this.$session.set("nickname", this.nickname)
            this.$store.dispatch("changeNickname", this.nickname)
            this.$router.push({
              path: '/profiles'
            })
          })
          .catch(err =>{
            console.log(err)
            alert("회원 정보 변경이 실패하였습니다. 잠시후 다시 시도해주십시오.")
          })
      },
      updatecancel () {
        this.$router.push({
          path: '/profiles'
        })
      }
    },
    mounted() {
      this.email = this.$store.getters.username
      this.nickname = this.$session.get("nickname")
    }
  }
</script>

<style scoped>
  #editprofile {
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
