<template>
  <div class="header">
    <div class="banner">
      <img src="../assets/image/bg.jpg" alt="">
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
    <br><br><br><br>
    <br><br><br><br>

    <div class="container">
      <div class="main-section">
        <h2 class="article-header my-5"><i class="fas fa-pen-nib" />인기 테마</h2>
        <!-- <revi-list limits="4" :themeData="themeData" /> -->
        <br>
      </div>

      <div class="main-section">
        <h2 class="article-header my-5"><i class="fas fa-pen-nib" />인기 여행지</h2>
        <!-- <revi-list limits="4" :spotData="spotData" /> -->
        <div class="hspot d-inline width:80% col-md-6 col-12">
          <div>
            <p :src="spotData[0]" width="300" height="300"></p>
            <p :src="spotData[1]" width="300" height="300"></p>
          </div>
          <div>
            <p :src="spotData[2]" width="300" height="300"></p>
            <p :src="spotData[3]" width="300" height="300"></p>
          </div>

        </div>
        <br>
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
        'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg',
        'https://cdn.vuetifyjs.com/images/carousel/bird.jpg',
        'https://cdn.vuetifyjs.com/images/carousel/planet.jpg',
        'https://cdn.vuetifyjs.com/images/carousel/sky.jpg'
      ],
      themeData: [

      ],
      spotData: [
        require('../assets/image/bg.jpg'),
        require('../assets/image/image01.jpg'),
        require('../assets/image/bg.jpg'),
        require('../assets/image/image01.jpg')
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
</style>
