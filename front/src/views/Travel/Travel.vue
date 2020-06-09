<template>
  <div id="travel">
    <!-- carousel -->
    <div class="travel-img-font">
      여행을 읽다<br>
      테마블러,
    </div>
    <v-carousel cycle height="60vw" hide-delimiter-background show-arrows-on-hover>
      <v-carousel-item v-for="slide in slides" :key="slide">
        <v-sheet height="100%">
          <v-row class="fill-height" align="center" justify="center">
            <img :src="slide" alt="" width="100%" />
          </v-row>
        </v-sheet>
      </v-carousel-item>
    </v-carousel>

    <!-- 여행지 -->
    <div class="pop-box">
      <div class="main-section">
        <h2 class="home-h2-title text-center ml-0"><i class="fas fa-book mr-4"></i>어디로 떠날까요?</h2>
        <v-sheet class="mx-auto theme-travel-box" max-width="100vw">
          <v-slide-group v-model="model" class="pa-4" center-active show-arrows>
            <v-slide-item v-for="theme in themeArr" :key="theme" v-slot:default="{ active, toggle }">
              <v-card class="home-destination-card" min-height="290px" max-height="30vw" min-width="218px" width="30vw"
                @click="toggle">
                <div>
                  <div class="home-card-destination-header">
                    <div class="home-card-title">
                      <i class="fas fa-book mr-1"></i>
                      {{ theme.name }}.tm
                    </div>
                    <i class="fas fa-window-close"></i>
                  </div>
                </div>
                <v-img @click="showDetail(theme.id)" :src="`${baseURL}/${theme.image}`" width="100%" height="100%" />
                <!-- <v-sheet class="d-flex justify-content-center align-items-center" @click="showDetail(theme.id)"
                  color="#546E7A" width="100%" height="100%" style="border-radius: 0;">
                  <div class="text-light pb-12" style="font-family: 'Cafe24Simplehae'; font-size: 25px;">
                    #.{{ theme.id }} {{ theme.region }}</div>
                </v-sheet> -->
                <v-row class="fill-height" align="center" justify="center">
                </v-row>
              </v-card>
            </v-slide-item>
          </v-slide-group>
        </v-sheet>

        <hr>

        <!-- destination -->
        <h3 class="home-h4-title text-center ml-0"><i class="fas fa-file-alt mr-4"></i>이 곳을 다닐거에요</h3>
        <div class="mb-12 travel-dests-box">
          <v-row class="d-flex justify-content-center">
            <v-col class="d-flex justify-content-center" v-for="dest in computedPageDestination" :key="dest.id"
              cols="12" lg="3" sm="6" xs="1">
              <v-card class="home-destination-card home-destination-card-sub row" min-height="290px" max-height="30vw"
                style="width: 100%;" @click="destsModal(dest.image, dest.name)">
                <div style="width: 100%;">
                  <div class="home-card-destination-header" style="width: 100%">
                    <div class="home-card-title">
                      <i class="fas fa-file-alt"></i>
                      {{dest.name}}.ds
                    </div>
                    <i class="fas fa-window-close"></i>
                  </div>
                </div>
                <v-img :src="`${baseURL}/${dest.image}`" width="100%" height="100%" />
                <v-row class="fill-height" align="center" justify="center">
                </v-row>
              </v-card>
            </v-col>
          </v-row>
        </div>
        <div class="d-inline" @click="getPaginationDestination">
          <v-pagination v-model="page" :length="pageLength" :total-visible="7"></v-pagination>
        </div>

        <!-- dests modal -->
        <v-dialog v-model="dialog" max-width="350">
          <v-card>
            <v-card-title class="headline d-flex justify-content-between"
              style="font-family: 'Cafe24Simplehae'!important; background: #2c3e50; color: white;">
              <div>{{ destName }}</div>
              <v-btn x-large icon @click="dialog = false"><i class="far fa-times-circle text-light"
                  style="font-style: 50px"></i></v-btn>
            </v-card-title>
            <v-img :src="`${baseURL}/${destImg}`" height="60vh"></v-img>
          </v-card>
        </v-dialog>
      </div>

      <!-- dests modal -->
      <v-dialog v-model="dialog" max-width="350">
        <v-card>
          <v-card-title class="headline d-flex justify-content-between"
            style="font-family: 'Cafe24Simplehae'!important; background: #2c3e50; color: white;">
            <div>{{ destName }}</div>
            <v-btn x-large icon @click="dialog = false"><i class="far fa-times-circle text-light"
                style="font-style: 50px"></i></v-btn>
          </v-card-title>
          <v-img :src="`${baseURL}/${destImg}`" height="60vh"></v-img>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: "Travel",
    data() {
      return {
        dialog: false,
        themeArr: [],
        destName: "",
        destImg: "",
        paginationDest: [],
        pageLength: 0,
        model: null,
        model_: null,
        page: 1,
        slides: [
          require("../../assets/bg1.jpg"),
          require("../../assets/bg5.jpg"),
        ],
        baseURL: process.env.VUE_APP_IP
      }
    },
    methods: {
      showDetail(themeId) {
        this.$router.push({
          path: `/travel/${themeId}`
        })
      },
      getPaginationDestination() {
        const token = this.$session.get("jwt")
        const requestHeader = {
          headers: {
            Authorization: "JWT " + token
          }
        }
        axios.get(`/travels/destinations/0/${this.page}/`, requestHeader)
          .then(response => {
            this.paginationDest = response.data.page_destination
            this.pageLength = response.data.all_length
          })
          .catch(err => {
            console.log(err)
          })
      },
      destsModal(img, name) {
        this.destImg = img
        this.destName = name
        this.dialog = true
      }
    },
    mounted() {
      const token = this.$session.get("jwt")
      const requestHeader = {
        headers: {
          Authorization: "JWT " + token
        }
      }
      axios.get('/travels/all_theme/', requestHeader)
        .then(response => {
          this.themeArr = response.data.all_theme
        })
        .catch(err => {
          console.log(err)
        })
      this.getPaginationDestination()
    },
    computed: {
      computedPageDestination() {
        return this.paginationDest
      }
    },
  }
</script>

<style lang="scss" scoped>
  #travel {
    padding-bottom: 5rem;
  }

  .travel-dests-box {
    width: 90vw;
    margin: 1rem auto 3rem auto;
  }

  @media (max-width: 275px) {
    .travel-dests-box {
      width: 85vw;
    }
  }

  .home-destination-card-sub {
    margin-bottom: 2.5rem;
  }

  .home-destination-card-sub:hover {
    opacity: .8;
  }

  .home-h4-title {
    font-family: 'Cafe24Simplehae';
    margin-top: 2rem;
    font-size: 35px;
  }

  .theme-travel-box {
    margin-bottom: 3rem;
  }

  .travel-img-font {
    position: absolute;
    top: 4%;
    left: 51%;
    z-index: 2;
    font-size: 8vw;
    font-weight: 700;
    font-style: italic;
    font-family: 'Cafe24Simplehae';
    color: white;
    text-shadow: black 1px 1px 1px;
  }

  .pop-box {
    margin-top: 32px;
    margin-bottom: 32px;
  }

  .main-section {
    margin-top: 0;
    margin-bottom: 0;
  }
</style>
