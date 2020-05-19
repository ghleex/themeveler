<template>
  <v-app id="profile">
    <Drawer class="drawer" d-flex />

    <v-container id="profile-content" fluid tag="section" d-flex>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <base-material-card>
            <template v-slot:heading>
              <div class="display-2 font-weight-light">
                Edit Profile
              </div>
              <div class="subtitle-1 font-weight-light">
                Complete your profile
              </div>
            </template>

            <v-form>
              <v-container class="py-0">
                <v-row>
                  <v-col cols="12">
                    <v-file-input label="Profile Image" class="purple-input" type="file" />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field label="Email" class="purple-input" disabled />
                  </v-col>
                  <v-col md="6">
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field label="Password" class="purple-input" />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field label="Password Confirm" class="purple-input" />
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-text-field label="User Name" class="purple-input" />
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-text-field label="First Name" class="purple-input" />
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-text-field label="Last Name" class="purple-input" />
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-text-field label="Gender" />
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-text-field label="Age" />
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-text-field label="Phone Number" />
                  </v-col>
                  <v-col cols="12">
                    <v-text-field label="Adress" class="purple-input" />
                  </v-col>
                  <!-- <v-col cols="12">
                    <v-textarea class="purple-input" label="About Me"
                      value="자기소개 문구 영역입니다."/>
                  </v-col> -->
                  <v-col cols="12" md="6" class="text-left" >
                    <v-btn color="red" class="mr-0" @click="userdelete">회원탈퇴</v-btn>
                  </v-col>
                  <v-col cols="12" md="6" class="text-right" >
                    <v-btn color="success" class="mr-4" @click="update">수정</v-btn>
                    <v-btn color="success" class="mr-0" @click="updatecancel">취소</v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
          </base-material-card>
        </v-col>

        <v-col cols="12" md="4">
          <base-material-card
            class="v-card-profile"
            avatar="https://demos.creative-tim.com/vue-material-dashboard/img/marc.aba54d65.jpg"
          >
            <v-card-text class="text-center">
              <h6 class="display-1 mb-1 grey--text">CO-FOUNDER</h6>
              <h4 class="display-2 font-weight-light mb-3 black--text">Alec Thompson</h4>
              <p class="font-weight-light grey--text">
                Don't be scared of the truth because we need to restart the human foundation in truth And I love you...
              </p>
              <v-btn color="success" rounded class="mr-0">Ream More</v-btn>
            </v-card-text>
          </base-material-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import Drawer from '../components/Drawer.vue'

export default {
  name: 'Profile',
  components: {
    Drawer
  },
  data() {
    return {
      dialog: false
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
      this.$router.push({
        path: '/profile'
      })
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
#profile {
  margin-top: 64px;
}

#profile-content {
  margin-left: 256px;
  width: 80%;
}
</style>
