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
                  <v-slide-item v-for="(img) in cardBypopTheme(model)" :key="img">
                    <v-card class="ma-4 popTheme-sub-img" height="123" width="120">

                      <!-- modal -->
                      <v-dialog v-model="dialog" width="500">
                        <template v-slot:activator="{ on }">
                          <v-img :src="img" v-on="on" height="123"></v-img>
                        </template>
                        <!-- <v-card v-if="img == img[index]"> -->
                        <v-card>
                          <v-img :src="img"></v-img>
                          <v-card-actions style="justify-content: flex-end;">
                            <v-btn color="#2c3e50" class="text-light" @click="dialog = false">
                              확인
                            </v-btn>
                          </v-card-actions>
                        </v-card>
                      </v-dialog>

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
    <div style="text-align: end;">
      <v-btn class="home-more-bt text-light" color="#2c3e50">MORE</v-btn>
    </div>


    <!-- 인기 여행지 -->
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








      <br><br><br><br><br><br>
      <div class="main-section">
        <br><br><br><br><br><br>
        <h2 class="article-header my-5"><i class="fas fa-walking"></i> ?? <i class="fas fa-walking"></i></h2>
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
        <v-container fluid class="mx-auto" max-width="95%">
          <v-row dense>
            <v-col v-for="card in spotcards" :key="card.title" :cols="12" :sm="3">
              <v-hover v-slot:default="{ hover }">
                <v-card class="mx-auto" max-width="90%" :elevation="hover ? 12 : 2">
                  <v-img :src="card.src" class="white--text align-end"
                    gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)" height="200px">
                    <v-card-title v-text="card.title"></v-card-title>
                  </v-img>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn icon><v-icon color="red">mdi-heart-outline</v-icon></v-btn>
                    <v-btn icon><v-icon color="green">mdi-bookmark-outline</v-icon></v-btn>
                  </v-card-actions>
                </v-card>
              </v-hover>
            </v-col>
          </v-row>
        </v-container>
        <br><br>
      </div>

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
      dialog: false,
      model: null,
      eachContext: '',
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
          ]
        },
        {
          id: 4,
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
        require('../assets/image/pop2.jpg')
      ],
      themeData: [

      ],
      spotData: [
        require('../assets/image/bg.jpg'),
        require('../assets/image/image01.jpg'),
        require('../assets/image/bg.jpg'),
        require('../assets/image/image01.jpg')
      ],
      spotcards: [
        { title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 3 },
        { title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 3 },
        { title: 'Best airlines.', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 3 },
        { title: 'Favorite road trips.', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 3 }
      ]
    }
  },
  methods: {
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
    }
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
    height: 3.5vw;
    padding: 0 .5rem 2rem .5rem;
    font-size: .8rem;
  }

  .popTheme-context {
    font-size: 1rem;
    font-weight: 700;
  }
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

.themecard {
  text-align: left;
}
</style>
