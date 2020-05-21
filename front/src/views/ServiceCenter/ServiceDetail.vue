<template>
  <div id="service-detail">
    <div class="service-center-title">
      <i class="fas fa-exclamation-circle"></i>
      고객센터
    </div>

    <div class="service-body">
      <div class="service-body-header">
        <div class="service-detail-created-date">
          {{data.createddate}}
        </div>
        <div class="service-detail-title">
          <!-- <b>제목</b>:  -->
          {{data.title}}</div>
      </div>

      <!-- <a>{{data.id}}</a> -->
      <div class="service-detail-user mt-3"><i class="fas fa-user"></i> {{data.writer}}</div><br>

      <div class="service-content">{{data.content}}</div><br>

      <v-btn color="rgb(238, 240, 247)" class="btn-detail" @click="back"><i class="fas fa-bars mr-1"></i>목록</v-btn>
      <div class="service-detail-btn mt-12">
        <v-btn color="#2c3e50" class="text-light mr-4 btn-detail mb-2" @click="updateData">수정<i
            class="fas fa-edit ml-1"></i></v-btn>
        <v-btn color="error" class="btn-detail" @click="deleteData">삭제<i class="fas fa-minus-square ml-1"></i></v-btn>
      </div>
    </div>

    <!-- comment list -->
    <div class="comment-header">
      댓글
    </div>
    <div class="comment-header-top"></div>
    <div class="service-comment">
      <v-form ref="form" class="service-comment-form" v-model="valid" lazy-validation>
        <div class="strLen mb-2">{{resultRemian}}/500</div>
        <div class="survice-comment-input">
          <i class="far fa-comments mr-5 mt-2" style="font-size: 23px;"></i>
          <v-textarea color="#607D8B" rows="3" class="service-comment-write" outlined label="댓글을 작성하세요."
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
  import data from '@/views/ServiceCenter/data'

  export default {
    name: 'service-detail',
    data() {
      const index = this.$route.params.serviceId
      return {
        valid: false,
        data: data[index],
        index: index,
        commentRules: [
          v => (v && v.length <= 500) || '댓글은 최대 500자 이내로 작성해주세요.',
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
      deleteData() {
        data.splice(this.index, 1)
        this.$router.push({
          path: '/service'
        })
      },
      updateData() {
        this.$router.push({
          name: 'service-create',
          params: {
            serviceId: this.index
          }
        })
      },
      back() {
        this.$router.push({
          path: '/service'
        })
      }
    }
  }
</script>

<style scoped>
  #service-detail {
    background-color: rgb(238, 240, 247);
    height: 100%;
  }

  #service-detail .service-center-title {
    font-family: 'Cafe24Simplehae';
    font-size: 30px;
    margin: 8rem auto 0 auto;
    /* background-color: rgb(255, 187, 0); */
    width: 80%;
    border-radius: 7px 7px 0 0;
    box-shadow: 1px 1px 2px 1px rgb(100, 105, 109);
    background-color: rgb(255, 255, 255);
    padding: 2rem 2rem;
    text-align: start;
  }

  #service-detail .service-body {
    background-color: #fff;
    width: 80%;
    padding: 1.2rem 2rem;
    margin: 0 10% 5rem 10%;
    border-radius: 0 0 7px 7px;
    box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
  }

  .service-detail-title {
    font-family: 'Cafe24Simplehae';
    /* text-align: start; */
    font-size: 20px;
    font-weight: 700;
  }

  .service-detail-created-date {
    color: rgb(170, 170, 170);
    font-size: 13px;
    /* font-style: italic; */
  }

  .service-body-header {
    /* display: flex;
    justify-content: space-between; */
  }

  .service-detail-user {
    /* text-align: start; */
  }

  .service-content {
    width: 60%;
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
    font-size: 19px;
    font-family: 'Cafe24Simplehae';
  }

  /* comment */
  .comment-header {
    border-radius: 8px 8px 0 0;
    background-color: #2c3e50;
    width: 110px;
    padding: .5rem 0 .2rem 0;
    font-family: 'Cafe24Simplehae';
    margin: 0 auto;
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

  @media (max-width: 501px) {
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