<template>
  <div id="comment">
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
          <v-btn color="#2c3e50" :disabled="!valid" class="service-comment-submitBtn" @click="commentSubmit()">
            작성<i class="fas fa-comment ml-1"></i>
          </v-btn>
        </div>
      </v-form>
      <v-divider></v-divider>
      <div class="comment-list">
        <div class="comment-content" v-for="comment in commentList" :key="comment.id">
          {{ comment.manager }} - {{ comment.content }}
          <v-icon @click="commentUpdate(comment.id)">mdi-pen</v-icon>
        </div>
      </div>
    </div>
    <div class="comment-header-bottom"></div>
  </div>
</template>

<script>
export default {
  name: 'comment',
  data() {
    return {
      commentList: [],
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
    checkLen() {
      var letterLength = this.strLen.length;
      this.resultRemian = 0
      this.resultRemian = this.remain - letterLength
    },
    commentSubmit() {
      if (this.$session.get("staff") === true) {
        var commentForms = {
          "content": this.strLen,
          "manager": this.$store.getters.user_id,
          "voice": this.serviceId
        }
        const requestHeader = this.$store.getters.requestHeader
        axios.post(`/articles/manager_reply/${this.serviceId}/`, commentForms, requestHeader)
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
    },
    commentUpdate(commentId) {      
      if (this.$session.get("staff") === true) {
        var commentForms = {
          "content": this.strLen,
          "manager": this.$store.getters.user_id,
          "voice": this.serviceId
        }
        const requestHeader = this.$store.getters.requestHeader
        axios.put(`/articles/manager_reply/${this.serviceId}/${commentId}/`, commentForms, requestHeader)
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
  }
}
</script>

<style scoped>
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
      padding: 2rem 1.2rem .5rem 1.2rem;
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
