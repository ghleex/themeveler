<template>
  <div id="notice-detail">
    <div class="notice-title">
      <h4>공지사항</h4>
      <v-divider></v-divider>
    </div>
    <div class="notice-body">
      <div class="body1">
        <p class="notice-body-title"><strong>{{notice.title}}</strong></p>
      </div>
      <div class="body2">
        <p class="notice-writer"><i class="fas fa-user"></i> {{notice.writer}}</p>
        <p class="notice-createddate"><i class="far fa-clock"></i> {{notice.createddate.slice(0, 16)}}</p>
      </div>
      <div class="body3">
        <div class="notice-content">{{notice.content}}</div>
      </div>
      <div class="notice-detail-btn">
        <v-divider></v-divider>
        <v-btn color="warning" class="mr-4" @click="updateData">수정</v-btn>
        <v-btn color="error" class="mr-4" @click="deleteData">삭제</v-btn>
        <v-btn color="primary" @click="back">목록</v-btn>
      </div>
    </div>

    <!-- Comment -->
    <div class="comment-header">댓글</div>
    <div class="comment-header-top"></div>
    <div class="service-comment">
      <v-form ref="form" class="service-comment-form" v-model="valid" lazy-validation>
        <div class="strLen mb-2">{{resultRemian}}/500</div>
        <div class="survice-comment-input">
          <i class="far fa-comments mr-5 mt-2" style="font-size: 23px;"></i>
          <v-textarea color="#607D8B" class="service-comment-write" outlined label="댓글을 작성하세요."
            :rules="commentRules" v-model="strLen" @keyup="checkLen">
          </v-textarea>
        </div>
        <div class="service-comment-submitBtn-box">
          <v-btn color="#2c3e50" :disabled="!valid" class="service-comment-submitBtn">
            작성<i class="fas fa-comment ml-1"></i>
          </v-btn>
        </div>
      </v-form>
    </div>
    <div class="comment-header-bottom"></div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'notice-detail',
  data() {
    const index = this.$route.params.noticeId
    return {
      notice: [],
      index: index,
      valid: false,
      commentRules: [
        v => (v && v.length <= 500) || '댓글은 최대 500자 이내로 작성해주세요.'
      ],
      remain: 500,
      resultRemian: 500,
      strLen: ""
    }
  },
  methods: {
    deleteData() {
      axios.delete(`/articles/notice/${this.index}`)
        .then(
          this.$router.push({
            path: '/notice'
          })
        )
    },
    updateData() {
      this.$router.push({
        path: `/articles/notice/create/${this.index}`
      })
    },
    back() {
      this.$router.push({
        path: '/notice'
      })
    },
    checkLen() {
      var letterLength = this.strLen.length;
      this.resultRemian = 0
      this.resultRemian = this.remain - letterLength
    }
  },
  mounted() {
    axios.get(`/articles/notice/${this.index}/`)
      .then(response => {
        this.notice = response.data
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
.notice-createddate {
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
  padding: 2rem 0 1rem 2rem;
  box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
}
/* .service-comment-form {
  display: flex;
} */
.survice-comment-input {
  display: flex;
  margin-right: 5em;
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
@media (max-width: 500px) {
  .survice-comment-input {
    margin-right: 0;
  }
  .service-content {
    width: 100%;
  }
  .service-comment {
    padding: 2rem 1.2rem .5rem 1.2rem;
  }
  .service-comment-submitBtn {
    margin: 0;
  }
  .strLen {
    margin-right: 0 !important;
  }
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
.strLen {
  display: flex;
  justify-content: flex-end;
  margin-right: 5rem;
}
</style>
