<template>
  <div class="header">
    <div class="home-search-bar">
      <SearchBar />
    </div>
    <!-- Carousels Banner -->
    <div class="carousel banner">
      <v-carousel cycle height="480" hide-delimiter-background show-arrows-on-hover :show-arrows="false">
        <v-carousel-item v-for="(slide, i) in slides" :key="i" :src="slide">
        </v-carousel-item>
      </v-carousel>
    </div><br>

    <!-- describe card -->
    <div class="describe">
      <div class="describe-card-left"></div>
      <div class="describe-left">
        <img :src="ticket" alt="">
      </div>
      <div class="describe-middle">
        <i class="fas fa-bus-alt"></i>
      </div>
      <div class="describe-right">
        <div class="describe-text m-auto">
          <b>THEMEVELER</b>란?
        </div>
        <div class="describe-context">
          Themeveler는 Theme + Traveler의 합성어로써, <br>
          테마를 여행하다는 의미입니다.
        </div>
        <i class="fas fa-barcode"></i>
      </div>
      <div class="describe-card-right"></div>
    </div>
    <div class="slogan">
      <i class="fas fa-map-marker-alt mr-1"></i>
      여행을 쫓다 감각을 좇다 테마블러
    </div>

    <!-- 인기 테마 -->
    <div class="pop-box">
      <h2 class="home-h2-title"><i class="fas fa-bookmark mr-2"></i>인기 테마</h2>
      <v-sheet class="mx-auto" max-width="100vw">
        <v-slide-group v-model="model" center-active show-arrows>
          <v-slide-item v-for="theme in themeArr" :key="theme.id" v-slot:default="{ active, toggle }">
            <div @click="cardBypopTheme(model)">
              <v-card class="ma-4" min-height="320px" max-height="35vw" min-width="238px" max-width="30vw"
                @click="toggle">
                <v-img width="100%" height="100%" :src="`${baseURL}/${theme.image}`" min-height="260px"
                  max-height="18vw" />
                <v-card-title class="pop-card-title">
                  <div class="mx-auto text-light pop-theme-card-text">
                    <i class="fas fa-quote-left"></i>{{ theme.name }}<i class="fas fa-quote-right"></i>
                  </div>
                </v-card-title>
                <v-row class="fill-height" align="center" justify="center">
                </v-row>
              </v-card>
            </div>
          </v-slide-item>
        </v-slide-group>
        <!-- 아래쪽에 나타나는 부분 -->
        <v-expand-transition>
          <v-sheet v-if="model != null" color="grey lighten-4" height="350" width="95%" tile
            class="home-pop-theme-subBox mx-auto">
            <div class="pop-theme-disc">
              <!-- true인 id값의 eachContext만 가져오는 -->
              <v-text v-if="toggle == active ? cardBypopThemeContext(model) : false"></v-text>
              <div class="popTheme-context">
                "{{ eachContext }}"
              </div>
            </div>
            <v-row class="mt-0" align="center" justify="center">
              <div class="pop-sub-img">
                <v-sheet class="ml-0 mr-auto" max-width="90vw">
                  <v-slide-group class="pa-4 pop-theme-slide-group" center-active show-arrows>
                    <v-slide-item v-for="dest in destinations" :key="dest">
                      <v-card class="ma-4 popTheme-sub-img" height="123" width="120">
                        <!-- 이미지 -->
                        <v-img height="123" @click="openCardModal(dest)"
                          :src="`${baseURL}/${dest.image}`"></v-img>
                        <v-row class="fill-height" align="center" justify="center">
                        </v-row>
                      </v-card>
                    </v-slide-item>
                    <!-- modal -->
                    <v-dialog content-class="dest-picture-modal" v-model="dialog" width="500">
                      <v-card>
                        <!-- 이미지 -->
                        <v-card-title  class="headline d-flex justify-content-between" style="font-family: 'Cafe24Simplehae'!important; background: #2c3e50; color: white;">
                          #.{{ dests.id }} {{ dests.name }}
                          <v-btn x-large icon @click="dialog = false"><i class="far fa-times-circle text-light" style="font-style: 50px"></i></v-btn>
                        </v-card-title>
                        <v-img height="80vh" :src="`${baseURL}/${dests.image}`"></v-img>
                      </v-card>
                    </v-dialog>
                  </v-slide-group>
                </v-sheet>
              </div>
            </v-row>
            <div style="text-align: end;">
              <v-btn rounded large class="home-more-bt text-light" color="#2c3e50" @click="goTheme(model)">
                <i class="fas fa-book mr-1" style="color:tomato;"></i>
                여행하기
              </v-btn>
            </div>
          </v-sheet>
        </v-expand-transition>
      </v-sheet>
    </div>

    <HowToUse></HowToUse>
    <TopScroll></TopScroll>
  </div>
</template>

<script>
  import axios from 'axios'
  import SearchBar from '@/components/SearchBar.vue'
  import HowToUse from '@/components/HowToUse.vue'
  import TopScroll from '@/components/TopScroll.vue'

  export default {
    name: "Home",
    components: {
      SearchBar,
      HowToUse,
      TopScroll
    },
    data() {
      return {
        e1: 1,
        toggle: false,
        active: false,
        dialog: false,
        dests: [],
        model: null,
        model_: null,
        eachContext: "",
        slides: [
          require("../assets/image/bg.jpg"),
          require("../assets/image/bg2.jpg"),
        ],
        themeArr: [],
        destinations: [],
        ticket: require("../assets/themeveler.png"),
        baseURL: ""
      }
    },
    methods: {
      a() {
        document.querySelector("#footer").style.display = 'block'
      },
      cardBypopTheme(id) {
        const requestHeader = this.$store.getters.requestHeader
        axios.get(`/travels/destinations/${id+1}/0/`, requestHeader)
          .then(response => {
            this.destinations = response.data.destinations
          })
          .catch(err => {
            console.log(err)
          })
      },
      cardBypopThemeContext(id) {
        this.eachContext = this.themeArr[id].content
      },
      openCardModal(dest) {
        this.dests = dest
        this.dialog = true
      },
      goTheme(model) {
        var themeId = model + 1
        this.$router.push({
          path: `/travel/${themeId}`
        })
      }
    },
    mounted() {
      const requestHeader = this.$store.getters.requestHeader
      // 모든 테마 불러오기
      axios.get("/travels/all_theme/", requestHeader)
        .then(response => {
          this.themeArr = response.data.all_theme
        })
        .catch(err => {
          console.log(err)
        })

      this.baseURL = process.env.VUE_APP_IP

      this.a()
    }
  }
</script>

<style>
  .v-stepper {
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0) !important;
  }

  .v-stepper__header {
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0) !important;
  }

  .home-how-to-box {
    display: flex;
    width: 75vw;
    height: 400px;
    margin: 0 auto 0 auto;
  }

  .header .home-howTo-img {
    width: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    border-radius: 7px 0 0 7px;
    box-shadow: 1px 1px 5px 1px rgba(0, 0, 0, 0.2);
  }

  .header .home-howTo-img>img {
    margin: 0;
  }

  .header .home-howTo-boxBtn {
    width: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #2c3e50;
    border-radius: 0 7px 7px 0;
    box-shadow: 1px 1px 5px 1px rgba(0, 0, 0, 0.2);
  }

  .home-how-to {
    margin-bottom: 5rem;
    font-family: 'Cafe24Simplehae';
  }

  .slogan {
    color: #526579;
    font-size: 14px;
    text-align: end;
    margin-bottom: 5rem;
    margin-right: 5rem;
    margin-top: .3rem;
  }

  .pop-box {
    background-color: #fff;
    padding: 2rem 0;
    margin-bottom: 5rem;
  }

  .header {
    background-color: rgb(248, 248, 246);
  }

  @media (min-width: 750px) {
    .home-h2-title {
      font-size: 50px;
    }
  }

  .home-destination-card {
    margin: 0 1rem;
  }

  .home-card-destination-header {
    height: 36px;
    background-color: #2c3e50;
    border-radius: 4px 4px 0 0;
    color: white;
    display: flex;
    justify-content: space-between;
    padding: .5rem 1rem 0 1rem;
  }

  .main-section .v-card {
    box-shadow: 0 0 0 0 black;
    border: 1px 1px 1px 1px solid #2c3e50;
    border-radius: 5px;
  }

  .describe {
    display: flex;
    width: 86vw;
    height: 346px;
    margin: 5rem auto 0 auto;
    background: #2c3e50;
    border-radius: 5px;
    padding: 3rem 5% 3rem 15%;
    box-shadow: 0 1px 2px .1px rgb(99, 94, 94);
  }

  .describe-card-left {
    background-color: rgb(255, 89, 89);
    width: 10px;
    height: 250px;
    border-radius: 20px 0 0 20px;
  }

  .describe-card-right {
    background-color: rgb(255, 89, 89);
    width: 20px;
    height: 250px;
    border-radius: 0 20px 20px 0;
  }

  .describe-left {
    background-size: cover;
    background-color: #fff;
    width: 30%;
    height: 250px;
    border-right: dotted 2px white;
    border-radius: 0 20px 20px 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .describe-left>img {
    width: 80%;
  }

  .describe-middle {
    width: 80px;
    height: 250px;
    background-color: rgb(255, 210, 210);
    font-size: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 20px 0 0 20px;
    padding: 0 2rem;
    border-right: dotted white 1px;
  }

  .describe-middle>i {
    padding: .6rem;
    border-radius: 50px;
    background-color: tomato;
    color: white;
  }

  .describe-right {
    width: 60%;
    height: 250px;
    font-family: 'Cafe24Simplehae';
    padding: 4.7%;
    background-color: rgb(250, 249, 249);
  }

  .describe-right>i {
    font-size: 150px;
    height: 50px;
    overflow: hidden;
    display: flex;
    justify-content: flex-end;
  }

  .describe-text {
    font-size: 27px;
  }

  .describe-context {
    font-size: 22px;
  }

  @media (max-width: 900px) {
    .home-how-to-box {
      flex-direction: column;
      align-items: center;
    }

    .home-howTo-img {
      height: 1200px;
      border-radius: 7px 7px 0 0 !important;
    }

    .home-howTo-img>img {
      width: 140%;
    }

    .home-howTo-boxBtn {
      height: 400px;
      border-radius: 0 0 7px 7px !important;
    }

    .home-howTo-boxBtn>button {
      width: 200px;
    }

    .home-howTo-boxBtn span {
      width: 100%;
      font-size: 14px;
      white-space: normal;
    }

    .describe-text {
      font-size: 20px;
      padding-top: 1rem;
    }

    .describe-context {
      font-size: 18px;
    }

    .describe {
      padding: 2rem 1rem 0 1rem;
    }

    .describe-middle>i {
      font-size: 20px;
    }

    .describe-middle {
      padding: .4rem;
    }
  }

  .main-section {
    margin-bottom: 5rem;
  }

  .home-h2-title {
    font-family: 'Cafe24Simplehae';
    text-align: start;
    margin-left: 5rem;
  }

  .home-more-bt {
    margin-top: 2rem;
    margin-right: 3.2rem;
    font-size: 1.3vw;
  }

  @media (max-width: 750px) {
    .home-more-bt {
      font-size: 14px;
    }

    .header .home-howTo-img {
      width: 70%;
    }

    .header .home-howTo-boxBtn {
      width: 70%;
    }

    .home-howTo-img>img {
      width: 450px;
    }

    .describe {
      margin-top: 32px;
    }

    .slogan {
      margin-bottom: 32px;
    }
  }

  .popTheme-sub-img:hover {
    cursor: pointer;
    box-shadow: 1px 1px 8px 3px gray;
    transition: .3s;
  }

  .pop-theme-slide-group {
    background-color: #f5f5f5;
  }

  .popTheme-context {
    font-family: 'Cafe24Simplehae';
    font-size: 25px;
    font-style: italic;
    padding: 1rem 2rem 0 2rem;
  }

  .pop-theme-card-text {
    background: #2c3e50;
    font-size: 1.5vw;
    padding: .5rem;
    font-family: 'Cafe24Simplehae';
    white-space: nowrap;
  }

  .pop-theme-card-text>i {
    font-size: 15px;
    margin: 0 .3rem;
  }

  @media (max-width: 950px) {
    .pop-theme-card-text {
      background: #2c3e50;
      font-size: 15px;
      font-family: 'Cafe24Simplehae';
      display: flex;
      padding: .5rem 0 .3rem 0;
    }

    .pop-theme-card-text {
      padding: .3rem 0 0 0;
    }

    .pop-theme-card-text>i {
      font-size: 15px;
      margin: 0 .3rem;
      height: 3.5vw;
      padding: 0 .5rem 2rem .5rem;
      font-size: .8rem;
    }

    .popTheme-context {
      font-size: 1rem;
      font-weight: 700;
    }
  }

  .banner>img {
    width: 100%;
    margin-top: -15%;
  }

  .home-search-bar {
    position: absolute;
    top: 20rem;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 10;
  }

  @media (max-width: 520px) {
    .header .home-howTo-img {
      width: 100%;
    }

    .header .home-howTo-boxBtn {
      width: 100%;
    }

    .home-howTo-img>img {
      width: 350px;
    }

    .home-search-bar {
      width: 80%;
    }

    .describe-right {
      width: 80%;
    }

    .describe-left {
      display: none;
    }

    .describe-card-left {
      display: none;
    }

    .describe-middle {
      width: 70px;
      background-color: tomato;
    }

    .describe-middle>i {
      background-color: #4c5b6b;
    }

    .info-img {
      width: 330px;
    }
  }

  .info-img {
    margin-bottom: 2rem;
  }
</style>