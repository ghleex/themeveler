<template>
  <v-app id="editprofile">
    <Drawer class="drawer" />

    <v-content id="profile-content">
      <h2 class="content-title">회원정보수정</h2>
      <hr>
      <v-row justify="center">
        <v-col col="12" md="8">
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
                <v-col cols="12" md="6" class="content-col">
                  <v-text-field label="Password" class="purple-input" />
                </v-col>
                <v-col cols="12" md="6" class="content-col">
                  <v-text-field label="Password Confirm" class="purple-input" />
                </v-col>
                <v-col cols="12" md="6" class="content-col">
                  <v-text-field label="User Name" class="purple-input" />
                </v-col>
                <v-col cols="12" md="6" class="content-col">
                  <v-text-field label="Name" class="purple-input" />
                </v-col>
                <v-col cols="12" md="4" class="content-col">
                  <v-select :items="['남','여']" label="Gender"></v-select>
                </v-col>
                <v-col cols="12" md="4" class="content-col">
                  <v-text-field label="Date of birth" />
                  <!-- <v-menu ref="menu" :close-on-content-click="false" v-model="menu" :nudge-right="40" lazy
                    transition="scale-transition" offset-y full-width max-width="290px" min-width="100px">
                    <v-text-field slot="activator" v-model="date" label="Date of birth" readonly></v-text-field>
                    <v-date-picker ref="picker" v-model="date" :max="new Date().toISOString().substr(0, 10)"
                      min="1950-01-01" @change="datesave" ></v-date-picker>
                  </v-menu> -->
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

        <v-col col="12" md="4">
          <v-card-text class="text-center">
            <h6 class="display-1 mb-1 grey--text">ad.</h6>
            <h4 class="display-2 font-weight-light mb-3 black--text">Alec Thompson</h4>
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
import Drawer from '../components/Drawer.vue'

export default {
  name: 'editprofile',
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
#editprofile {
  margin-top: 64px;
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
