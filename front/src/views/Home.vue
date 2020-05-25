<template>
  <div class="header">
    <v-btn style="position:absolute; margin-top:70px; left:80%; z-index:2;" color="primary" outlined to="/profile">유저페이지>>>>임시버튼</v-btn>
    <div class="home-search-bar">
      <SearchBar />
    </div>
    <!-- Carousels Banner -->
    <div class="carousel banner">
      <v-carousel cycle height="480" hide-delimiter-background show-arrows-on-hover :show-arrows="false">
        <v-carousel-item v-for="(slide, i) in slides" :key="i" :src="slide">
        </v-carousel-item>
      </v-carousel>
    </div><br><br>

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
        <v-sheet v-if="model != null" color="grey lighten-4" height="250" width="95%" tile
          class="home-pop-theme-subBox mx-auto">
          <div class="pop-theme-disc">
            <v-text v-if="toggle == active ? cardBypopThemeContext(model):false"></v-text>
            <div class="popTheme-context">
              "{{ eachContext }}"
            </div>
          </div>
          <v-row class="mt-0" align="center" justify="center">
            <div class="pop-sub-img">
              <v-sheet class="ml-0 mr-auto" max-width="90vw">
                <v-slide-group class="pa-4 pop-theme-slide-group" center-active show-arrows>
                  <!-- <v-slide-item v-for="(img, index) in cardBypopTheme(model)" :key="img"> -->
                  <v-slide-item v-for="img in cardBypopTheme(model)" :key="img">
                    <v-card class="ma-4 popTheme-sub-img" height="123" width="120">
                      <v-img :src="img" height="123" @click="openCardModal(img)"></v-img>

                      <!-- modal -->

                      <v-row class="fill-height" align="center" justify="center">
                      </v-row>
                    </v-card>
                  </v-slide-item>

                  <v-dialog v-model="dialog" width="500">
                    <v-card>
                      <v-img :src="imgUrl" height="80vh" width="100vw"></v-img>
                      <!-- {{ img }} {{ index }} -->
                      <v-card-actions style="justify-content: flex-end;">
                        <v-btn color="#2c3e50" class="text-light" @click="dialog = false">
                          확인
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>

                </v-slide-group>
              </v-sheet>
            </div>
          </v-row>
        </v-sheet>
      </v-expand-transition>
    </v-sheet>
    <div style="text-align: end;">
      <v-btn class="home-more-bt text-light" color="#2c3e50">MORE</v-btn>
    </div>


    <!-- 인기 여행지 -->
    <div class="main-section">
      <h2 class="home-h2-title mt-12"><i class="fas fa-bus-alt mr-2"></i>인기 여행지</h2>
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
        toggle: false,
        active: false,
        dialog: false,
        imgUrl: '',
        model: null,
        eachContext: "",
        popTheme: [{
            id: 0,
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
            id: 1,
            img: require('../assets/image/pop2.jpg'),
            title: '서울사람도 잘 몰라',
            context: '일단 아무말이나 적어보자.',
            imgs: [
              require('../assets/image/pop2sub1.jpg'),
              require('../assets/image/pop2sub2.jpg'),
              require('../assets/image/pop2sub3.jpg'),
              require('../assets/image/pop2sub4.jpg'),
              require('../assets/image/pop2sub5.jpg'),
            ]
          },
          {
            id: 2,
            img: require('../assets/image/pop3.jpg'),
            title: '홍콩 어디까지 가봤니?',
            context: '홍콩 에그타르트 JMT.',
            imgs: [
              require('../assets/image/pop3sub1.jpg'),
              require('../assets/image/pop3sub2.jpg'),
              require('../assets/image/pop3sub3.jpg'),
              require('../assets/image/pop3sub4.jpg'),
              require('../assets/image/pop3sub5.jpg'),
            ]
          },
          {
            id: 3,
            img: require('../assets/image/pop4.jpg'),
            title: '최고의 디즈니 랜드',
            context: '도쿄는 생각보다 별롭니다. 플로리다 올랜도는 쩔어요. 가장 큰 디즈니 월드(world) 클라쓰~',
            imgs: [
              require('../assets/image/pop4sub1.jpg'),
              require('../assets/image/pop4sub2.jpg'),
              require('../assets/image/pop4sub3.jpg'),
              require('../assets/image/pop4sub4.jpg'),
              require('../assets/image/pop4sub5.jpg'),
            ]
          },
          {
            id: 4,
            img: require('../assets/image/pop5.jpg'),
            title: '혼저옵서예',
            context: '유일한 제주 남부의 시장을 가면 싱싱한 회 팩이 마치 3만원!',
            imgs: [
              require('../assets/image/pop5sub1.jpg'),
              require('../assets/image/pop5sub2.jpg'),
              require('../assets/image/pop5sub3.jpg'),
              require('../assets/image/pop5sub4.jpg'),
              require('../assets/image/pop5sub5.jpg'),
            ]
          },
        ],
        slides: [
          require('../assets/image/bg.jpg'),
          require('../assets/image/bg-3.jpg'),
        ],
      }
    },
    methods: {
      a() {
        document.querySelector('#footer').style.display = 'block'
      },
      cardBypopTheme(id) {
        var theme = this.popTheme.filter(theme => {
          return theme.id == id
        })
        // console.log(theme[0].imgs)
        return theme[0].imgs
      },
      cardBypopThemeContext(id) {
        var theme = this.popTheme.filter(theme => {
          return theme.id == id
        })
        // console.log(theme[0].context)
        this.eachContext = theme[0].context
      },
      openCardModal(imgUrl) {
        console.log(imgUrl)
        this.imgUrl = imgUrl
        this.dialog = true
      }
    },
    mounted() {
      this.a()
    },
    cardBypopThemeContext(id) {
      var theme = this.popTheme.filter(theme => {
        return theme.id == id
      })
      // console.log(theme[0].context)
      this.eachContext = theme[0].context
    }
  }
</script>

<style scoped>
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
    /* font-style: italic; */
  }

  .pop-theme-card-text>i {
    font-size: 15px;
    margin: 0 .3rem;
    /* display: flex; */
    /* align-items: flex-start; */
  }

  /* media query가 좀 이상하게 작동 함 */
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
    .home-search-bar {
      width: 80%;
    }
  }

  @media (max-width: 520px) {
    .home-search-bar {
      width: 80%;
    }
  }
</style>
