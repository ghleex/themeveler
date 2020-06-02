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
          <div class="like-theme text-center" @click="likeTheme()">
            {{ likeCount }} <br>
            <i v-if="like == false" class="far fa-heart"></i>
            <i v-else-if="like == true" class="fas fa-heart text-danger"></i>
          </div>
        </div>
        <div class="theme-detail-go text-end">
          <v-btn color="red" @click="goThemeStory()" dark rounded><b>GO!</b><i class="fas fa-play-circle ml-1"></i>
          </v-btn>
        </div>
      </div>
      <ChatBot :themeId=themeId />
    </div>

    <v-btn class="my-5" to="/travel/" rounded dark color="#2c3e50">📃뒤로가기</v-btn>

    <!-- destinations -->
    <div class="text-center mx-3" width="100%">
      <div class="d-flex mt-5 justify-content-center">
        <v-btn class="btn-round-num mr-2" v-model="destination" color="red" dark rounded v-if="model != null">
          {{ model + 1 }}
        </v-btn>
        <div v-if="model >= 0">{{ destination }}</div>
      </div>
    </div>

    <v-sheet class="theme-detail-destination mx-auto d-flex justify-content-center" max-width="100vw"
      style="margin-bottom: 5rem;">
      <v-slide-group v-model="model" class="pa-4" center-active show-arrows>
        <v-slide-item v-for="destination in destinations" :key="destination" v-slot:default="{ active, toggle }">
          <v-card class="ma-4" height="200" width="180" @click="toggle">

            <!-- 이미지가 없으므로 임시 card -->
            <v-sheet @click="toggleDestination(destination)" class="d-flex justify-content-center align-items-center"
              color="#9575CD" width="100%" height="100%" style="border-radius: 0;">
              <div class="text-light pb-8" style="font-family: 'Cafe24Simplehae'; font-size: 25px;">
                #.{{ destination.id }} {{ destination.name }}</div>
            </v-sheet>

            <v-row class="fill-height" align="center" justify="center">
            </v-row>
          </v-card>
        </v-slide-item>
      </v-slide-group>
    </v-sheet>
  </div>
</template>

<script>
  import axios from 'axios'
  import ChatBot from '../../components/ChatBot.vue'

  export default {
    name: 'TravelDetail',
    components: {
      ChatBot,
    },
    props: {
      themeId: Number
    },
    data() {
      return {
        toggle: false,
        themeArr: [],
        destinations: [],
        model: null,
        date: "",
        time: "",
        like: false,
        destination: "",
        likeCount: 0,
        likeUsers: [],
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
        this.destination = destination.name
      },
      goThemeStory() {
        this.$router.push(`/travel/${this.themeId}/start`)
      }
    },
    mounted() {
      const token = this.$session.get("jwt")
      const requestHeader = {
        headers: {
          Authorization: "JWT " + token
        }
      }
      axios.get("/travels/all_theme/", requestHeader)
        .then(res => {
          this.themeArr = res.data.all_theme

          var dateTime = res.data.all_theme[this.themeId - 1].created_at
          this.date = dateTime.substr(0, 10)
          this.time = dateTime.substr(11, 5)
          // console.log(this.date)
          // console.log(this.time)

          // console.log(this.themeArr)
        })

      axios.get(`/travels/destinations/${this.themeId}`, requestHeader)
        .then(res => {
          this.destinations = res.data.destinations
          // console.log(res.data)
        })

      axios.get(`/travels/like/${this.themeId}`, requestHeader)
        .then(res => {
          this.likeCount = res.data.like_users_count
          this.likeUsers = res.data.like_users
        })

      axios.get(`/travels/like/${this.themeId}`, this.themeId, requestHeader)
        .then(res => {
          console.log(res.data)
        })
        .catch(err =>
        console.log(err.response))
    }
  }
</script>

<style lang="scss" scoped>
  .theme-detail-origin-box {}

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