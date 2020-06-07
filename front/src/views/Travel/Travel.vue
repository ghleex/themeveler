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
    <div class="pop-box mt-8">
      <div class="main-section">
        <h2 class="home-h2-title text-center ml-0"><i class="fas fa-book mr-4"></i>어디로 떠날까요?</h2>
        <v-sheet class="mr-auto" max-width="90vw">
          <v-slide-group v-model="model" class="pa-4" center-active show-arrows>
            <v-slide-item v-for="theme in themeArr" :key="theme" v-slot:default="{ active, toggle }">
              <v-card class="home-destination-card" min-height="290px" max-height="30vw" min-width="218px" width="30vw"
                @click="toggle">
                <div>
                  <div class="home-card-destination-header">
                    <div class="home-card-title">
                      <i class="fas fa-book mr-1"></i>
                      {{ theme.name }}.exe
                    </div>
                    <i class="fas fa-window-close"></i>
                  </div>
                </div>

                <v-img @click="showDetail(theme.id)" :src="'http://localhost:8000/uploads/theme/'+theme.name+'.jpg'" width="100%" height="100%" />
                <!-- 임시 -->
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

        <div class="mb-12" style="width: 90vw; margin: 1rem auto 3rem auto;">
          <v-row class="d-flex justify-content-center">
            <v-col class="d-flex justify-content-center" v-for="dest in paginationDest" :key="dest.id" cols="12" lg="3" sm="6" xs="1">
              <v-card class="home-destination-card row" min-height="290px" max-height="30vw" style="width: 100%;" @click="toggle">
                <div style="width: 100%;" class="">
                  <!-- <div class="home-card-destination-name pt-2 text-light">여행지</div> -->
                  <div class="home-card-destination-header" style="width: 100%">
                    <div class="home-card-title">
                      <i class="fas fa-file-alt"></i>
                      {{dest.name}}
                    </div>
                    <i class="fas fa-window-close"></i>
                  </div>
                </div>
                <v-img :src="dest.image" width="100%" height="100%" />
                <v-row class="fill-height" align="center" justify="center">
                </v-row>
              </v-card>
            </v-col>
          </v-row>
        </div>
        <div class="d-inline" @click="getPaginationDestination">
          <v-pagination v-model="page" :length="pageLength" :total-visible="7"></v-pagination>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: "Travel",
    data() {
      return {
        themeArr: [],
        paginationDest: [],
        pageLength: 0,
        model: null,
        model_: null,
        page: 1,
        slides: [
          require("../../assets/bg1.jpg"),
          require("../../assets/bg5.jpg"),
        ],
        // destination: [
        //   require('../../assets/image/destination1.jpg'),
        //   require('../../assets/image/destination2.jpg'),
        //   require('../../assets/image/destination3.jpg'),
        //   require('../../assets/image/destination4.jpg'),
        //   require('../../assets/image/destination1.jpg'),
        //   require('../../assets/image/destination2.jpg'),
        //   require('../../assets/image/destination3.jpg'),
        //   require('../../assets/image/destination4.jpg'),
        // ],
      }
    },
    methods: {
      showDetail(themeId) {
        this.$router.push(`/travel/${themeId}`)
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
      this.getPaginationDestination()
    }
  }
</script>

<style lang="scss" scoped>
  #travel {
    padding-bottom: 5rem;
  }

  .travel-img-font {
    position: absolute;
    top: 8%;
    left: 51%;
    z-index: 2;
    font-size: 8vw;
    font-weight: 700;
    font-style: italic;
    font-family: 'Cafe24Simplehae';
    color: white;
    text-shadow: black 1px 1px 1px;
  }
</style>
