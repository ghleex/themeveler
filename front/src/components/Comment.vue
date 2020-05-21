<template>
  <div id="comment">
      <!-- Comment -->
    <div class="comment-header">댓글</div>
    <div class="comment-header-top"></div>
    <div class="service-comment">
      <v-form ref="form" class="service-comment-form" v-model="valid" lazy-validation>
        <i class="far fa-comments mr-5 mt-2" style="font-size: 23px;"></i>
        <v-textarea color="#607D8B" class="service-comment-write" outlined label="댓글을 작성하세요." :rules="commentRules">
        </v-textarea>
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
export default {
  name: 'comment',
  data() {
    return {
      valid: false,
      commentRules: [
        v => (v && v.length <= 500) || '댓글은 최대 500자 이내로 작성해주세요.'
      ]
    }
  },
  methods: {

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

.service-comment-form {
  display: flex;
}

.service-comment-submitBtn-box {
  display: flex;
  align-items: flex-end;
  height: 150px;
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
</style>
