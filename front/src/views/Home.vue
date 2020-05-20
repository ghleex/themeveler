<template>
  <div class="home-box">
    <div class="home-search-bar">
      <SearchBar />
    </div>

    <!-- Carousels -->
    <div class="carousel">
      <v-carousel cycle height="400px" hide-delimiters hide-delimiter-background show-arrows-on-hover>
        <v-carousel-item v-for="(slide, i) in slides" :key="i" :src="slide">
        </v-carousel-item>
      </v-carousel>
    </div>

    <v-btn color="primary" class="mt-6" outlined to="/profile">
      유저페이지>>>>임시버튼</v-btn>

    <!-- 인기 테마 -->
    <h2 class="home-h2-title"><i class="fas fa-bookmark mr-2"></i>인기 테마</h2>
    <v-sheet class="mx-auto" max-width="100vw">
      <v-slide-group v-model="model" center-active show-arrows>
        <v-slide-item v-for="pt in popTheme" :key="pt.title" v-slot:default="{ active, toggle }">
          <v-card class="ma-4" min-height="320px" max-height="35vw" min-width="238px" max-width="30vw" @click="toggle">
            <v-img :src="pt.img" min-height="260px" max-height="18vw" />
            <v-card-title class="pop-card-title">
              <div class="mx-auto text-light pop-theme-card-text"><i class="fas fa-quote-left"></i>{{pt.title}}<i
                  class="fas fa-quote-right"></i></div>
            </v-card-title>
            <v-row class="fill-height" align="center" justify="center">
            </v-row>
          </v-card>
        </v-slide-item>
      </v-slide-group>

      <v-expand-transition>
        <v-sheet v-if="model != null" color="grey lighten-4" height="300" tile class="home-pop-theme-subBox">
          <div class="pop-theme-disc">
            <!-- {{pt.context}} {{model}} -->
          </div>
          <v-row class="fill-height" align="center" justify="center">
            <div class="pop-sub-img">
              <v-sheet class="ml-0 mr-auto" max-width="90vw">
                <v-slide-group class="pa-4" center-active show-arrows>
                  <v-slide-item v-for="i in 4" :key="i">
                    <v-card class="ma-4" height="100" width="100">
                      <!-- <v-img :src="popTheme.imgs[i]"></v-img> -->
                      <v-row class="fill-height" align="center" justify="center">
                      </v-row>
                    </v-card>
                  </v-slide-item>
                </v-slide-group>
              </v-sheet>
            </div>
          </v-row>
        </v-sheet>
      </v-expand-transition>
    </v-sheet>















    <div class="main-section">
      <h2 class="home-h2-title mt-12"><i class="fas fa-bus-alt mr-2"></i>인기 여행지</h2>

      <!-- <revi-list limits="4" :spotData="spotData" /> -->
      <!-- <div class="hspot d-inline width:80% col-md-6 col-12">
          <div>
            <p :src="spotData[0]" width="300" height="300"></p>
            <p :src="spotData[1]" width="300" height="300"></p>
          </div>
          <div>
            <p :src="spotData[2]" width="300" height="300"></p>
            <p :src="spotData[3]" width="300" height="300"></p>
          </div>
        </div>
        <br> -->
      <!-- 인기 여행지 Card -->
      <!-- <v-container fluid class="mx-auto" max-width="95%">
          <v-row dense>
            <v-col v-for="card in cards" :key="card.title" :cols="card.flex">
              <v-card class="mx-auto" max-width="90%">
                <v-img :src="card.src" class="white--text align-end"
                  gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)" height="200px">
                  <v-card-title v-text="card.title"></v-card-title>
                </v-img>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn icon>
                    <v-icon>mdi-heart</v-icon>
                  </v-btn>
                  <v-btn icon>
                    <v-icon>mdi-bookmark</v-icon>
                  </v-btn>
                  <v-btn icon>
                    <v-icon>mdi-share-variant</v-icon>
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-container> -->
      <br><br>
    </div>
  </div>

</template>

<script>
  import SearchBar from '../components/SearchBar.vue'

  export default {
    name: 'Home',
    components: {
      SearchBar,
    },
    data() {
      return {
        model: null,
        popTheme: [{
            img: require('../assets/image/pop1.webp'),
            title: '타지 사람들 집합',
            context: '지역 사람들만 아는 숨겨진 맛집과 명소를 소개합니다.',
            imgs: [
              require('../assets/image/pop1sub1.jpg'),
              require('../assets/image/pop1sub2.jpg'),
              require('../assets/image/pop1sub3.jpg'),
              require('../assets/image/pop1sub4.jpg'),
              require('../assets/image/pop1sub5.jpg'),
            ]
          },
          {
            img: require('../assets/image/pop2.jpg'),
            title: '서울사람도 잘 몰라',
            context: '일단 아무말이나 적어보자.',
            imgs: []
          },
          {
            img: require('../assets/image/pop3.jpg'),
            title: '홍콩 어디까지 가봤니?',
            context: '홍콩 에그타르트 JMT.',
            imgs: []
          },
          {
            img: require('../assets/image/pop4.jpg'),
            title: '최고의 디즈니 랜드',
            context: '도쿄는 생각보다 별롭니다. 플로리다 올랜도는 쩔어요. 가장 큰 디즈니 월드(world) 클라쓰~',
            imgs: []
          },
          {
            img: require('../assets/image/pop5.jpg'),
            title: '혼저옵서예',
            context: '유일한 제주 남부의 시장을 가면 싱싱한 회 팩이 마치 3만원!',
            imgs: []
          },
        ],
        popImg: [
          require('../assets/image/pop1.webp'),
          require('../assets/image/pop2.jpg'),
          require('../assets/image/pop3.jpg'),
          require('../assets/image/pop4.jpg'),
          require('../assets/image/pop5.jpg'),
        ],
        slides: [
          require('../assets/image/bg.jpg'),
          require('../assets/image/bg-3.jpg'),
        ],
        themeData: [

        ],
        // cards: [{
        //     title: 'Pre-fab homes',
        //     src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg',
        //     flex: 3
        //   },
        //   {
        //     title: 'Favorite road trips',
        //     src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg',
        //     flex: 3
        //   },
        //   {
        //     title: 'Best airlines',
        //     src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg',
        //     flex: 3
        //   },
        //   {
        //     title: 'Favorite road trips.',
        //     src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg',
        //     flex: 3
        //   },
        //   {
        //     title: 'Pre-fab homes.',
        //     src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg',
        //     flex: 3
        //   },
        //   {
        //     title: 'Best airlines.',
        //     src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg',
        //     flex: 3
        //   },
        //   {
        //     title: 'Favorite road trips..',
        //     src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg',
        //     flex: 3
        //   },
        //   {
        //     title: 'Best airlines..',
        //     src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg',
        //     flex: 3
        //   }
        // ]
      }
    },
    methods: {
      a() {
        document.querySelector('#footer').style.display = 'block'
      }
    },
    mounted() {
      this.a()
    }
  }
</script>

<style scoped>
  .pop-theme-card-text {
    background: #2c3e50;
    font-size: 1.5vw;
    padding: .5rem;
    font-family: 'Cafe24Simplehae';
    /* font-style: italic; */
  }

  .pop-theme-card-text>i {
    font-size: 15px;
    margin: 0 .3rem;
    /* display: flex; */
    /* align-items: flex-start; */
  }

  .home-h2-title {
    font-family: 'Cafe24Simplehae';
    text-align: start;
    margin-left: 4rem;
    font-size: 40px;
  }

  @media (max-width: 950px) {
    .pop-theme-card-text {
      height: 5vw;
      padding: 0 .5rem 2rem .5rem;
    }
  }

  .banner>img {
    width: 100%;
    /* max-height: initial; */
    margin-top: -15%;
  }

  .home-search-bar {
    position: absolute;
    top: 20rem;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 10;
  }

  .themecard {
    text-align: left;
  }
</style>