<template>
  <v-app id="editprofile">
    <Drawer class="drawer" />

    <v-content id="profile-content">
      <h2 class="content-title">회원정보수정</h2>
      <hr>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-form>
            <v-container class="py-0">
              <v-row>
                <v-col cols="12" class="content-col">
                  <v-file-input label="Profile Image" class="purple-input" type="file" />
                </v-col>
                <v-col cols="12" md="6" class="content-col">
                  <v-text-field label="Email (ID)" class="purple-input" disabled />
                </v-col>
                <v-col md="6" class="content-col">
                </v-col>
                <!-- <v-col cols="12" md="6" class="content-col">
                  <v-text-field label="Password" class="purple-input" />
                </v-col>
                <v-col cols="12" md="6" class="content-col">
                  <v-text-field label="Password Confirm" class="purple-input" />
                </v-col> -->
                <v-col cols="12" md="6" class="content-col">
                  <v-text-field v-model="nickname" label="Nickname" class="purple-input" />
                </v-col>
                <v-col cols="12" md="6" class="content-col">
                  <v-text-field label="Name" class="purple-input" />
                </v-col>
                <v-col cols="12" md="4" class="content-col">
                  <v-select :items="['남','여']" label="Gender"></v-select>
                </v-col>
                <v-col cols="12" md="4" class="content-col">
                  <v-text-field label="Date of birth" />
                </v-col>
                <v-col cols="12" md="4" class="content-col">
                  <v-text-field label="Phone Number" />
                </v-col>
                <v-col cols="12" class="content-col">
                  <v-text-field label="Address" class="purple-input" />
                </v-col>
                <v-col cols="4" md="6" class="text-left">
                  <v-btn color="red" class="mr-0" @click="userdelete">회원탈퇴</v-btn>
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
import axios from "axios"
import Drawer from '@/components/Drawer.vue'

export default {
  name: 'editprofile',
  components: {
    Drawer
  },
  data() {
    return {
      dialog: false,
      nickname: ""
    }
  },
  methods: {
    userdelete() {
      var result = confirm("정말로 회원을 탈퇴하시겠습니까?")
      if (result) {
        this.$router.push({
          path: '/'
        })
      }
      else {
        this.$router.push({
          path: '/profile'
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
          this.$router.push('/profile')
        })
        .catch(err =>{
          console.log(err)
          alert("회원 정보 변경이 실패하였습니다. 잠시후 다시 시도해주십시오.")
        })
    },
    updatecancel () {
      this.$router.push({
        path: '/profile'
      })
    }
  },
  mounted() {
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
