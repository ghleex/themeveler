<template>
  <div class="theme-detail-origin-box">
    <div class="themeDetail-box">
      <div class="theme-detail-left">
      </div>
      <div class="theme-detail-right">
        <div class="theme-detail-title">
          <i class="fas fa-quote-left mr-1"></i>
          <h2>{{ themeArr[themeId-1].name }}</h2>
          <i class="fas fa-quote-right ml-1"></i>
        </div>
        <div class="theme-detail-content">
          <i class="fas fa-map-marker-alt mr-3"></i><b>지역</b><br>
          {{ themeArr[themeId-1].region }} <br><br>

          <i class="fas fa-thumbtack mr-2"></i><b>내용</b><br>
          {{ themeArr[themeId-1].content }} <br><br>
          <div class="text-center">
            <i style="color: gray;">{{ date }} <br> {{ time }}</i>
            <br><br>
          </div>
          <div class="like-theme text-center">
            {{ likeCount }} <br>
            <i @click="likeTheme()" v-if="like == false" class="far fa-heart"></i>
            <i @click="likeTheme()" v-else-if="like == true" class="fas fa-heart text-danger"></i>
          </div>
        </div>
        <div class="theme-detail-go text-end">
          <v-btn color="red" @click="goThemeStory()" dark rounded><b>GO!</b><i class="fas fa-play-circle ml-1"></i>
          </v-btn>
        </div>
      </div>
      <ChatBot :themeId=themeId :themeName=themeName />
    </div>

    <v-btn class="my-5" to="/travel/" rounded dark color="#2c3e50">📃뒤로가기</v-btn>



    <!-- destinations -->
    <div style="margin: 3rem 0 1rem 0">
      <div v-if="model == null" class="text-gray text-center mb-4" style="font-size: 12px;">
        * 이미지를 클릭하면 장소를 알 수 있어요!
      </div>
      <div class="text-center" width="100%">
        <div class="d-flex justify-content-center">
          <v-btn class="btn-round-num mr-2" v-model="destination" color="red" dark rounded v-if="model != null">
            {{ model + 1 }}
          </v-btn>
          <div v-if="model >= 0">{{ destination }}</div>
        </div>
      </div>
    </div>

    <v-sheet class="theme-detail-destination mx-auto d-flex justify-content-center" max-width="100vw"
      style="margin-bottom: 5rem;">
      <v-slide-group v-model="model" class="pa-4" center-active show-arrows>
        <v-slide-item v-for="destination in destinations" :key="destination.title" v-slot:default="{ active, toggle }">
          <v-card class="ma-4" height="200" width="180" @click="toggle">

            <!-- 이미지가 없으므로 임시 card -->
            <v-sheet @click="toggleDestination(destination)" class="d-flex justify-content-center align-items-center"
              color="#37474F" width="100%" height="100%" style="border-radius: 0;">
              <div class="text-light pb-8" style="font-family: 'Cafe24Simplehae'; font-size: 25px;">
                #.{{ destination.id }} {{ destination.name }}</div>
            </v-sheet>

            <v-row class="fill-height" align="center" justify="center">
            </v-row>
          </v-card>
        </v-slide-item>
      </v-slide-group>
    </v-sheet>


    <!-- detination modal -->
    <v-dialog v-model="dialog" max-width="350">
      <v-card>
        <v-card-title class="headline">
          여행지 이름
        </v-card-title>

        <v-card-text>
          댓글,, 어쩌구
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn rounded color="red" text @click="dialog = false" style="background: #FFEBEE;">
            나가기
            <i class="fas fa-sign-out-alt ml-1"></i>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import axios from 'axios'
  import ChatBot from '@/components/ChatBot.vue'

  export default {
    name: "TravelDetail",
    components: {
      ChatBot,
    },
    props: {
      themeId: Number,
      themeName: String,
    },
    data() {
      return {
        toggle: false,
        themeArr: [{
          "name": "name"
        }, ],
        destinations: [],
        model: null,
        date: "",
        time: "",
        like: false,
        destination: "",
        likeCount: 0,
        dialog: false,
      }
    },
    methods: {
      likeTheme() {
        const requestHeader = this.$store.getters.requestHeader
        axios.post(`/travels/like/${this.themeId}/`, this.themeId, requestHeader)
          .then(res => {
            this.like = res.data.isLiked
          })
        if (this.like == false) {
          this.likeCount += 1
        } else {
          this.likeCount -= 1
        }
      },
      toggleDestination(destination) {
        this.dialog = true
        this.destination = destination.name
      },
      goThemeStory() {
        this.$router.push(`/travel/${this.themeId}/start`)
      }
    },
    mounted() {
      const requestHeader = this.$store.getters.requestHeader
      axios.get("/travels/all_theme/", requestHeader)
        .then(res => {
          this.themeArr = res.data.all_theme
          this.themeName = this.themeArr[this.themeId - 1].name
          // console.log(this.themeName)

          var dateTime = res.data.all_theme[this.themeId - 1].created_at
          this.date = dateTime.substr(0, 10)
          this.time = dateTime.substr(11, 5)
          // console.log(this.date)
          // console.log(this.time)

          // console.log(this.themeArr)
        })

      axios.get(`/travels/destinations/${this.themeId}/0`, requestHeader)
        .then(res => {
          this.destinations = res.data.destinations
          // console.log(res.data)
        })
      // .catch(err => {
      //   console.log(err.response)
      // })

      axios.get(`/travels/like/${this.themeId}`, requestHeader)
        .then(res => {
          this.likeCount = res.data.like_users_count
          this.like = res.data.did_user_like
        })
      // .catch(err => {
      //   console.log(err.response)
      // })
      document.querySelector("#footer").style.display = 'block'
    }
  }
</script>

<style lang="scss" scoped>
  .theme-detail-origin-box {
    background-color: #ECEFF1;
    height: 100%;
  }

  .theme-detail-destination {
    margin-bottom: 15rem !important;
  }

  .btn-round-num {
    min-width: 35px !important;
    border-radius: 50px;
    padding: 0 !important;
  }

  .like-theme>i {
    cursor: pointer;
    font-size: 25px;
    transition: .5s;
  }

  .themeDetail-box {
    display: flex;
    font-family: 'Cafe24Simplehae';
    z-index: 1;
  }

  .theme-detail-left {
    width: 55vw;
    height: 37vw;
    margin: 8rem 0 5rem 10%;
    background-image: url("../../assets/image/daegu.jpg");
    background-size: cover;
    border-radius: 3px 0 0 3px;
    box-shadow: 1px 1px 3px 1px rgb(187, 184, 184);
  }

  .theme-detail-right {
    z-index: 1;
    width: 30vw;
    height: 37vw;
    margin: 8rem 10% 5rem 0;
    border-radius: 0 3px 3px 0;
    box-shadow: 1px 1px 3px 1px rgb(187, 184, 184);
    background-color: #fff;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
    padding: 1rem;
  }

  .theme-detail-title {
    display: flex;
    justify-content: center;
    // align-items: center;
    background-color: #2c3e50;
    color: white;
    padding: .5rem .5rem 0 .5rem;
    margin-bottom: 1rem;
  }

  .theme-detail-title>i {
    font-size: 18px;
  }


  .theme-detail-content {
    width: 80%;
    text-align: start;
  }

  .theme-detail-content>b {
    font-size: 20px;
  }

  .theme-detail-go {
    width: 95%;
  }

  @media (max-width: 1230px) {
    .themeDetail-box {
      flex-direction: column;
    }

    .theme-detail-left {
      border-radius: 3px 3px 0 0;
      margin: 8rem auto 0 auto;
      width: 80vw;
      height: 60vw;
    }

    .theme-detail-right {
      border-radius: 0 0 3px 3px;
      margin: 0 auto 1rem auto;
      width: 80vw;
      height: inherit;
      padding: 2rem;

    }
  }
</style>