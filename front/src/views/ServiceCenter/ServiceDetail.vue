<template>
  <div id="service-detail">
    <div class="service-center-title">
      <i class="fas fa-exclamation-circle mr-3"></i>고객센터
    </div>
    <div class="service-body">
      <div class="service-body-header">
        <div class="service-detail-title">{{ serviceData.title }}</div>
      </div>
      <div class="body">
        <p class="service-writer"><i class="fas fa-user"></i> {{ serviceData.request_user_nickname }}</p>
        <p class="service-created-date"><i class="far fa-clock"></i> {{ serviceData.created_at | moment("YYYY-MM-DD LT") }}</p>
      </div>
      <div class="service-content mt-3">{{ serviceData.content }}</div><br>
      <div class="service-detail-btn mt-12">
        <v-btn color="warning" class="text-light mr-4 btn-detail" @click="updateData">수정 <i class="fas fa-edit ml-1"></i></v-btn>
        <v-btn color="error" class="mr-4 btn-detail" @click="deleteData">삭제 <i class="fas fa-minus-square ml-1"></i></v-btn>
        <v-btn color="rgb(238, 240, 247)" class="btn-detail" @click="back">목록 <i class="fas fa-bars ml-1"></i></v-btn>
      </div>
    </div>

    <!-- Comment -->
    <div class="comment-header">관리자 댓글</div>
    <div class="comment-header-top"></div>
    <div class="service-comment">
      <v-form ref="form" class="service-comment-form" v-model="valid" lazy-validation v-if="isAuthenticated">
        <div class="strLen mb-2">{{ resultRemian }}/500</div>
        <div class="survice-comment-input">
          <i class="far fa-comments mr-5 mt-2" style="font-size: 23px;"></i>
          <v-textarea color="#607D8B" rows="3" class="service-comment-write" outlined label="댓글을 작성하세요."
            :rules="commentRules" v-model="addComment" @keyup="checkLen">
          </v-textarea>
        </div>
        <div class="service-comment-submitBtn-box">
          <v-btn color="#2c3e50" :disabled="!valid" class="service-comment-submitBtn" @click="commentSubmit">
            작성<i class="fas fa-comment ml-1"></i>
          </v-btn>
        </div>
      </v-form>
      <v-divider v-if="isAuthenticated"></v-divider>
      <div class="comment-list">
        <div class="comment-content" v-for="comment in commentList" :key="comment.id">
          <div v-if="modifyState === true">
            <v-text-field v-model="comment.content"></v-text-field>
            <v-icon @click="commentUpdate(comment)">mdi-pen</v-icon>
          </div>
          <div v-else>
            {{ comment.manager_name }} - {{ comment.content }}
            <v-icon @click="modify">mdi-pen</v-icon>
          </div>
        </div>
      </div>
    </div>
    <div class="comment-header-bottom"></div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "service-detail",
  data() {
    return {
      serviceData: [],
      serviceId: "",
      userId: "",
      commentList: [],
      valid: false,
      commentRules: [
        v => (v && v.length <= 500) || '댓글은 최대 500자 이내로 작성해주세요.'
      ],
      remain: 500,
      resultRemian: 500,
      addComment: "",
      isAuthenticated: this.$session.get("staff"),
      modifyState: false
    }
  },
  methods: {
    deleteData() {
      if (this.serviceData.request_user_id === this.$store.getters.user_id) {
        const requestHeader = this.$store.getters.requestHeader
        axios.delete(`/articles/voice/${this.serviceId}/`, requestHeader)
          .then(() => {
            this.$router.push({
              path: '/service'
            })
          })
          .catch(err => {
            console.log(err)
          })
      } else {
        alert("삭제 권한이 없습니다.")
        this.$router.push(`/service/detail/${this.serviceId}`)  
      }
    },
    updateData() {
      this.$router.push({
        path: `/service/create/${this.serviceId}`
      })
    },
    back() {
      this.$router.push({
        path: '/service'
      })
    },
    checkLen() {
      var letterLength = this.addComment.length
      this.resultRemian = 0
      this.resultRemian = this.remain - letterLength
    },
    commentSubmit() {
      if (this.$session.get("staff") === true) {
        var commentForms = {
          "content": this.addComment,
          "manager": this.$store.getters.user_id,
          "voice": this.serviceId
        }
        const requestHeader = this.$store.getters.requestHeader
        axios.post(`/articles/manager_reply/${this.serviceId}/`, commentForms, requestHeader)
          .then(response => {
            this.commentList.unshift(response.data)
          })
          .catch(err => {
            console.log(err)
          })
      }
      else {
        alert("권한이 없습니다.")
      }
    },
    modify() {
      if (this.$session.get("staff") === true) {
        this.modifyState = true
      }
      else {
        alert("권한이 없습니다.")
      }
    },
    commentUpdate(comment) {
      if (this.$session.get("staff") === true) {
        this.modifyState = false
        var commentForms = {
          "content": comment.content,
          "manager": this.$store.getters.user_id,
          "voice": this.serviceId
        }
        const requestHeader = this.$store.getters.requestHeader
        axios.put(`/articles/manager_reply/${this.serviceId}/${comment.id}/`, commentForms, requestHeader)
          .then(response => {
            console.log(response.data)
          })
          .catch(err => {
            console.log(err)
          })
      }
      else {
        alert("권한이 없습니다.")
      }
    }
  },
  mounted() {
    this.serviceId = this.$route.params.serviceId
    this.userId = this.$store.getters.user_id
    const requestHeader = this.$store.getters.requestHeader
    axios.get(`/articles/voice/${this.serviceId}/`, requestHeader)
      .then(response => {
        this.serviceData = response.data
        this.commentList = response.data["replys"]
      })
      .catch(err => {
        console.log(err)
      })
  }
}
</script>

<style scoped>
  #service-detail {
    height: 100%;
    background-color: rgb(238, 240, 247);
  }

  #service-detail .service-center-title {
    font-family: 'Cafe24Simplehae';
    font-size: 30px;
    background-color: rgb(255, 255, 255);
    margin: 80px auto 0 auto;
    width: 80%;
    border-radius: 7px 7px 0 0;
    box-shadow: 1px 1px 2px 1px rgb(100, 105, 109);
    padding: 2rem 2rem;
    text-align: start;
  }

  #service-detail .service-body {
    background-color: #fff;
    width: 80%;
    padding: 1.2rem 1rem;
    margin: 0 auto 60px auto;
    border-radius: 0 0 7px 7px;
    box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
  }

  @media (max-width: 600px) {
    #service-detail .service-center-title {
      width: 95%;
    }

    #service-detail .service-body {
      width: 95%;
    }
  }

  .service-body-header {
    text-align: left;
    margin-left: 5%;
  }

  .service-detail-title {
    font-family: 'Cafe24Simplehae';
    font-size: 20px;
    font-weight: 700;
  }

  .body {
    text-align: right;
    margin-right: 5%;
  }

  .service-writer {
    display: inline;
    font-size: 14px;
    color:gray;
  }

  .service-created-date {
    display: inline;
    font-size: 14px;
    color:gray;
    margin-left: 8px;
  }

  .service-content {
    width: 90%;
    background-color: #d0d7df49;
    border-radius: 5px;
    border: 1px solid #2c3e5049;
    text-align: start;
    padding: 1rem;
    margin: 0 auto;
  }

  .service-detail-btn {
    display: flex;
    justify-content: flex-end;
    width: 100%;
    border-top: rgb(231, 231, 231) 1px solid;
    padding-top: 1.5rem
  }

  .btn-detail {
    font-size: 16px;
    font-family: 'Cafe24Simplehae';
  }

  .comment-header {
    border-radius: 8px 8px 0 0;
    background-color: #2c3e50;
    width: 110px;
    padding: .5rem 0 .2rem 0;
    font-family: 'Cafe24Simplehae';
    color: white;
    font-size: 20px;
    margin: 0 auto 0 12.5%;
    box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
  }

  .comment-header-top {
    height: 5px;
    width: 75%;
    background-color: #2c3e50;
    font-size: 19px;
    margin: 0 auto 0 auto;
    border-radius: 0 3px 0 0;
    box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
  }

  .service-comment {
    background-color: #fff;
    width: 75%;
    margin: 0 auto 0 auto;
    padding: 1rem 0 1rem 2rem;
    box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
  }

  .strLen {
    display: flex;
    justify-content: flex-end;
    margin-right: 2rem;
  }

  .survice-comment-input {
    display: flex;
    margin-right: 2em;
  }

  .service-comment-submitBtn-box {
    display: flex;
    align-items: flex-start;
    justify-content: flex-end;
    margin-bottom: 1rem;
    margin-right: 1rem;
  }

  .service-comment-submitBtn {
    color: white;
    font-size: 19px;
    font-family: 'Cafe24Simplehae';
    margin: 0 1rem;
  }

  .service-comment-write {
    width: 80%;
  }

  .comment-header-bottom {
    height: 20px;
    width: 75%;
    background-color: #2c3e50;
    font-size: 19px;
    margin: 0 auto 5rem auto;
    border-radius: 0 0 3px 3px;
    box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
  }

  @media (max-width: 600px) {
    .comment-header {
      margin: 0 auto 0 5%;
    }

    .comment-header-top {
      width: 90%;
    }

    .strLen {
      margin-right: 0 !important;
    }

    .survice-comment-input {
      margin-right: 0;
    }

    .service-content {
      width: 100%;
    }

    .service-comment {
      width: 90%;
      padding: 1rem 1.2rem 1rem 1.2rem;
    }

    .service-comment-submitBtn-box {
      margin-right: 0;
    }

    .service-comment-submitBtn {
      margin: 0;
    }

    .comment-header-bottom {
      width: 90%;
    }
  }

  .comment-list {
    text-align: left;
  }

  .comment-content {
    width: 95%;
    background-color: #d0d7df49;
    border-radius: 5px;
    border: 1px solid #2c3e5049;
    text-align: start;
    padding: 1rem;
  }

  @media (max-width: 600px) {
    .comment-content {
      width: 100%;
    }
  }
</style>
