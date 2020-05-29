<template>
  <div class="theme-detail-origin-box">
    <div class="themeDetail-box">
      <div class="theme-detail-left">
      </div>
      <div class="theme-detail-right">
        <div class="theme-detail-title">
          <i class="fas fa-quote-left mr-1"></i>
          <h1>{{ themeArr[themeId-1].name }}</h1>
          <i class="fas fa-quote-right ml-1"></i>
        </div>
        <div class="theme-detail-content">
          <i class="fas fa-map-marker-alt mr-3"></i><b>지역</b><br>
          {{ themeArr[themeId-1].region }} <br><br>

          <i class="fas fa-thumbtack mr-2"></i><b>내용</b><br>
          {{ themeArr[themeId-1].content }} <br><br>
          <div class="text-end">
            <i style="color: gray;">{{ themeArr[themeId-1].created_at }}</i>
            <br><br>
          </div>
          <div class="theme-detail-go">
            <v-btn color="red" rounded><b>GO!</b><i class="fas fa-play-circle ml-1"></i></v-btn>
          </div>
        </div>
      </div>
      <ChatBot />
    </div>
    <h3 class="mb-10">그리고 여기 아래에 나오는 5가지 테마,,, Go를 누르면 stpper 시작과 길 안내</h3>
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
        themeArr: [],
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
        .then(response => {
          this.themeArr = response.data.all_theme
          // console.log(this.themeArr)
        })
    }
  }
</script>

<style lang="scss" scoped>
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
    border-radius: 10px 0 0 10px;
    box-shadow: 1px 1px 3px 1px rgb(187, 184, 184);
  }

  .theme-detail-right {
    z-index: 1;
    width: 30vw;
    height: 37vw;
    margin: 8rem 10% 5rem 0;
    border-radius: 0 10px 10px 0;
    box-shadow: 1px 1px 3px 1px rgb(187, 184, 184);
    background-color: #fff;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
  }

  .theme-detail-title {
    display: flex;
    justify-content: center;
    // align-items: center;
    background-color: #2c3e50;
    color: white;
    padding: .5rem .5rem 0 .5rem;
  }
  .theme-detail-title > i {
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
    text-align: end;
  }

  @media (max-width: 850px) {
    .themeDetail-box {
      flex-direction: column;
    }

    .theme-detail-left {
      border-radius: 10px 10px 0 0;
      margin: 8rem auto 0 auto;
      width: 80vw;
      height: 60vw;
    }

    .theme-detail-right {
      border-radius: 0 0 10px 10px;
      margin: 0 auto 5rem auto;
      width: 80vw;
      height: 25vw;
      padding: 1rem;

    }
  }
</style>