<template>
  <div class="theme-detail-origin-box">
    <div class="themeDetail-box">
      <div class="theme-detail-left">
        <v-img :src="`${baseURL}/${themeArr[themeId-1].image}`" width="inherit" height="inherit">
        </v-img>
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
            <div v-if="isAuthenticated">
              <i @click="likeTheme()" v-if="like == false" class="far fa-heart"></i>
              <i @click="likeTheme()" v-else-if="like == true" class="fas fa-heart text-danger"></i>
            </div>
            <div v-else>
              <i @click="requireLogin()" class="far fa-heart"></i>
            </div>
          </div>
        </div>
        <div class="theme-detail-go text-end">
          <div v-if="isAuthenticated">
            <v-btn color="red" @click="goThemeStory()" dark rounded><b>GO!</b><i class="fas fa-play-circle ml-1"></i></v-btn>
          </div>
          <div v-else>
            <v-btn color="red" @click="requireLogin()" dark rounded><b>GO!</b><i class="fas fa-play-circle ml-1"></i></v-btn>
          </div>
        </div>
      </div>
      <ChatBot :themeId=themeId :themeName=themeName v-if="isAuthenticated" />
      <ChatBot v-else @click="requireLogin()" />
    </div>
    <v-btn class="my-5" to="/travel/" rounded dark color="#2c3e50">📃뒤로가기</v-btn>

    <!-- destinations -->
    <!-- <div style="margin: 3rem 0 1rem 0">
      <div v-if="model == null" class="text-gray text-center mb-4" style="font-size: 12px;">
        * 이미지를 클릭하면 장소를 알 수 있어요!
      </div>
      <div class="text-center" width="100%">
        <div class="d-flex justify-content-center">
          <v-btn class="btn-round-num mr-2" v-model="destsName" color="red" dark rounded v-if="model != null">
            {{ model + 1 }}
          </v-btn>
          <div v-if="model >= 0">{{ destsName }}</div>
        </div>
      </div>
    </div> -->

    <v-sheet class="theme-detail-destination" max-width="100vw">
      <v-slide-group v-model="model" class="pa-4" center-active show-arrows>
        <v-slide-item v-for="(destination, index) in destinations" :key="destination.title" v-slot:default="{ active, toggle }">
          <v-card class="ma-4" height="200" width="180" @click="toggleDestination(index)">
            <div @click="toggle" class="card-title-img">
              <v-card-title class="detail-destination-title text-light">
                <b>{{ index + 1 }}.</b> {{ destination.name }}
              </v-card-title>
              <v-img @click="toggleDestination(index)" :src="`${baseURL}/${destination.image}`" width="100%" height="100%">
              </v-img>
              <v-row class="fill-height" align="center" justify="center">
              </v-row>
            </div>
          </v-card>
        </v-slide-item>
      </v-slide-group>
    </v-sheet>

    <!-- detination modal -->
    <v-dialog content-class="dest-picture-modal" v-model="dialog" max-width="350">
      <v-card>
        <v-card-title class="headline d-flex justify-content-between" style="font-family: 'Cafe24Simplehae'!important; background: #2c3e50; color: white;">
          <div>#{{ model + 1 }}. {{ destsName }}</div>
          <v-btn x-large icon @click="dialog = false"><i class="far fa-times-circle text-light" style="font-style: 50px"></i></v-btn>
        </v-card-title>
        <v-img :src="destImg" height="80vh"></v-img>
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
      ChatBot
    },
    props: {
      themeId: Number,
      themeName: String
    },
    data() {
      return {
        toggle: false,
        themeArr: [{
          "name": "name"
        }],
        destinations: [],
        model: null,
        date: "",
        time: "",
        like: false,
        destination: "",
        likeCount: 0,
        dialog: false,
        destId: 0,
        destsName: "",
        destImg: "",
        isAuthenticated: this.$session.get("jwt"),
        baseURL: process.env.VUE_APP_IP
      }
    },
    methods: {
      likeTheme() {
        const requestHeader = this.$store.getters.requestHeader
        axios.post(`/travels/like/${this.themeId}/`, this.themeId, requestHeader)
          .then(response => {
            this.like = response.data.isLiked
          })
        if (this.like == false) {
          this.likeCount += 1
        } else {
          this.likeCount -= 1
        }
      },
      toggleDestination(id) {
        this.destsName = this.destinations[id].name
        this.destImg = `${this.baseURL}/${this.destinations[id].image}`
        this.dialog = true
      },
      goThemeStory() {
        this.$router.push({
          path: `/travel/${this.themeId}/start`
        })
      },
      requireLogin() {
        alert("로그인 후 이용해주세요.")
      }
    },
    mounted() {
      document.scrollingElement.scrollTop = 0
      const requestHeader = this.$store.getters.requestHeader
      axios.get("/travels/all_theme/", requestHeader)
        .then(response => {
          this.themeArr = response.data.all_theme
          this.themeName = this.themeArr[this.themeId - 1].name
          var dateTime = response.data.all_theme[this.themeId - 1].created_at
          this.date = dateTime.substr(0, 10)
          this.time = dateTime.substr(11, 5)
        })

      axios.get(`/travels/destinations/${this.themeId}/0/`, requestHeader)
        .then(response => {
          this.destinations = response.data.destinations
        })

      axios.get(`/travels/like/${this.themeId}/`, requestHeader)
        .then(response => {
          this.likeCount = response.data.like_users_count
          this.like = response.data.did_user_like
        })

      document.querySelector("#footer").style.display = "block"
    }
  }
</script>

<style>
  .card-title-img {
    height: inherit;
    width: inherit;
  }

  .dest-picture-modal::-webkit-scrollbar {
    width: 5px;
  }

  .dest-picture-modal::-webkit-scrollbar-thumb {
    background: #2c3e50;
    border-radius: 10px;
  }

  .theme-detail-origin-box {
    background-color: #ECEFF1;
    height: 100%;
  }

  .theme-detail-destination {
    display: flex;
    justify-content: center;
    margin: 3rem auto 3rem auto;
  }

  .detail-destination-title {
    margin-left: auto;
    margin-right: auto;
    width: auto;
    top: 35%;
    left: 0;
    right: 0; 
    justify-content: center; 
    position: absolute;
    z-index: 5;
    background: rgba(0, 0, 0, 0.6); 
    font-family: 'Cafe24Simplehae';
    font-size: 15px;
    border-top-right-radius: 0 !important;
    border-top-left-radius: 0 !important;
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

  @media (max-width: 1320px) {
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
