<template>
  <div class="header">
    <div class="banner">
      <img src="../assets/image/bg.jpg" alt="">
      <v-btn style="position:absolute; margin-top:70px; left:80%; z-index:2;" color="primary" outlined to="/profile">유저페이지>>>>임시버튼</v-btn>
    </div>
    <div class="home-search-bar">
      <SearchBar />
    </div>


    <!-- Carousels -->
    <div class="carousel">
      <v-carousel cycle height="500" hide-delimiter-background show-arrows-on-hover>
        <v-carousel-item v-for="(slide, i) in slides" :key="i" :src="slide">
          <v-sheet width="100%">
            <v-row class="fill-height" align="center" justify="center">
              <div></div>
              <!-- <div class="display-3">{{ slide }} Slide</div> -->
            </v-row>
          </v-sheet>
        </v-carousel-item>
      </v-carousel>
    </div>
    <br>
    <br>


    <div class="container">
      <div class="main-section">
        <h2 class="article-header my-5">인기 테마 <i class="fas fa-walking"></i></h2>
        <!-- <revi-list limits="4" :themeData="themeData" /> -->
        <!-- <br> -->
        <!-- 인기 테마 Card -->
        <v-container fluid :cols="4" class="d-inline">
          <v-row dense>
            <v-card class="mx-auto my-2 themecard" max-width="30%">
              <v-img class="white--text align-end" height="200px" src="https://cdn.vuetifyjs.com/images/cards/docks.jpg">
                <v-card-title>Top 10 Daejeon Theme</v-card-title>
              </v-img>
              <v-card-subtitle class="pb-0">Number 10</v-card-subtitle>
              <v-card-text class="text--primary">
                <div>Whitehaven Beach</div>
                <div>Whitsunday Island, Whitsunday Islands</div>
              </v-card-text>
              <v-card-actions>
                <v-btn color="orange" text>Share</v-btn>
                <v-btn color="orange" text>Explore</v-btn>
              </v-card-actions>
            </v-card>

            <v-card class="mx-auto my-2 themecard" max-width="30%">
              <v-img class="white--text align-end" height="200px" src="https://cdn.vuetifyjs.com/images/cards/docks.jpg">
                <v-card-title>Top 10 Seoul Theme</v-card-title>
              </v-img>
              <v-card-subtitle class="pb-0">May 15</v-card-subtitle>
              <v-card-text class="text--primary">
                <div>City</div>
                <div>City, Seoul</div>
              </v-card-text>
              <v-card-actions>
                <v-btn color="orange" text>Share</v-btn>
                <v-btn color="orange" text>Explore</v-btn>
              </v-card-actions>
            </v-card>
            <v-card class="mx-auto my-2 themecard" max-width="30%">
              <v-img class="white--text align-end" height="200px" src="https://cdn.vuetifyjs.com/images/cards/docks.jpg">
                <v-card-title>Top 10 Gangwon-do Theme</v-card-title>
              </v-img>
              <v-card-subtitle class="pb-0">May 15</v-card-subtitle>
              <v-card-text class="text--primary">
                <div>City</div>
                <div>City, Gangwon-do</div>
              </v-card-text>
              <v-card-actions>
                <v-btn color="orange" text>Share</v-btn>
                <v-btn color="orange" text>Explore</v-btn>
              </v-card-actions>
            </v-card>
          </v-row>
        </v-container>
      </div>


      <div class="main-section">
        <h2 class="article-header my-5">인기 여행지 <i class="fas fa-walking"></i></h2>
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
                    <!-- <v-btn icon><v-icon>mdi-share-variant</v-icon></v-btn> -->
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
      slides: [
        require('../assets/image/bg.jpg'),
        require('../assets/image/squirrel.jpg'),
        require('../assets/image/sky.jpg'),
        require('../assets/image/planet.jpg'),
        require('../assets/image/sky.jpg'),
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
        { title: 'Pre-fab homes', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 3 },
        { title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 3 },
        { title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 3 },
        { title: 'Favorite road trips.', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 3 },
        { title: 'Pre-fab homes.', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 3 },
        { title: 'Best airlines.', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 3 },
        { title: 'Favorite road trips..', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 3 },
        { title: 'Best airlines..', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 3 }
      ]
    }
  },
  // methods: {
  //   a() {
  //     document.querySelector('#footer').style.display = 'flex'
  //   }
  // },
  // mounted() {
  //   this.a()
  // }
}
</script>

<style scoped>
.banner {
  position: relative;
  overflow: hidden;
  height: 500px;
}
.banner>img {
  width: 100%;
  /* max-height: initial; */
  margin-top: -15%;
}
.home-search-bar {
  position: absolute;
  top: 20vw;
  left: 50%;
  transform: translate(-50%, -50%);
}
.themecard {
  text-align: left;
}
</style>
