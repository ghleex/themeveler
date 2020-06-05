<template>
  <div id="notice-detail">
    <div class="notice-title">
      <h4>공지사항</h4>
      <v-divider></v-divider>
    </div>
    <div class="notice-body">
      <div class="body1">
        <p class="notice-body-title"><strong>{{ noticeData.title }}</strong></p>
      </div>
      <div class="body2">
        <p class="notice-writer"><i class="fas fa-user"></i> {{ noticeData.writer_nickname }}</p>
        <p class="notice-created-date"><i class="far fa-clock"></i> {{ noticeData.writed_at | moment('YYYY-MM-DD HH:mm') }}</p>
      </div>
      <div class="body3">
        <div class="notice-content">{{ noticeData.content }}</div>
      </div>
      <div class="notice-detail-btn">
        <v-divider></v-divider>
        <v-btn color="warning" class="mr-4 btn-detail" @click="updateData" v-if="isAuthenticated">수정<i class="fas fa-edit ml-1"></i></v-btn>
        <v-btn color="error" class="mr-4 btn-detail" @click="deleteData" v-if="isAuthenticated">삭제<i class="fas fa-minus-square ml-1"></i></v-btn>
        <v-btn color="rgb(238, 240, 247)" class="btn-detail" @click="back">목록<i class="fas fa-bars ml-1"></i></v-btn>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "notice-detail",
  data() {
    return {
      noticeData: [],
      noticeId: "",
      isAuthenticated: this.$session.get("staff")
    }
  },
  methods: {
    deleteData() {
      if (this.noticeData.writer === this.$store.getters.user_id) {
        const requestHeader = this.$store.getters.requestHeader
        axios.delete(`/articles/theme_notice/${this.noticeId}/`, requestHeader)
          .then(() => {
            this.$router.push({
              path: '/notice'
            })
          })
          .catch(err => {
            console.log(err)
          })
      } else {
        alert("삭제 권한이 없습니다.")
      }
    },
    updateData() {
      if (this.noticeData.writer === this.$store.getters.user_id) {
        this.$router.push({
          path: `/notice/create/${this.noticeId}`
        })
      } else {
        alert("수정 권한이 없습니다.")
      }
    },
    back() {
      this.$router.push({
        path: '/notice'
      })
    }
  },
  mounted() {
    this.noticeId = this.$route.params.noticeId
    axios.get(`/articles/notices/${this.noticeId}/`)
      .then(response => {
        this.noticeData = response.data
      })
      .catch(err => {
        console.log(err)
      })
  }
}
</script>

<style scoped>
  #notice-detail {
    text-align: center;
    height: 100%;
  }

  .notice-title {
    margin: 80px auto 0 auto;
    text-align: start;
    width: 80%;
    font-family: 'Cafe24Simplehae';
    font-size: 30px;
  }

  .notice-body {
    margin: 0 auto 60px auto;
    text-align: center;
    width: 80%;
  }

  .notice-title>h4 {
    text-align: left;
    margin: 8px;
  }

  .body1 {
    text-align: left;
  }

  .notice-body-title {
    display: inline;
    margin-left: 8px;
    font-family: 'Cafe24Simplehae';
    font-size: 20px;
    font-weight: 700;
  }

  .body2 {
    text-align: right;
  }

  .notice-writer {
    display: inline;
    font-size: 14px;
    color:gray;
  }

  .notice-created-date {
    display: inline;
    font-size: 14px;
    color:gray;
    margin-left: 8px;
  }

  .body3 {
    min-height: 250px;
  }

  .notice-content {
    text-align: left;
    margin: 8px;
    max-height: 100
  }

  .notice-detail-btn {
    text-align: right;
  }

  .btn-detail {
    font-size: 16px;
    font-family: 'Cafe24Simplehae';
  }
</style>
