<template>
  <div id="notice-create">
    <div class="notice-title">공지사항 작성</div>
    <div class="notice-body">
      <div class="reset">
        <v-btn color="error" outlined class="btn" @click="reset"><i class="fas fa-redo-alt mr-1"></i>다시 작성</v-btn>
      </div>
      <v-form ref="form" class="notice-create-form" v-model="valid" lazy-validation>
        <v-select v-model="select" :items="categorys" :rules="categoryRules" label="분류" required></v-select>
        <v-text-field v-model="title" :counter="30" :rules="titleRules" label="제목" required></v-text-field>
        <v-textarea v-model="content" :rules="contentRules" label="내용" class="mt-4" outlined></v-textarea>
        <v-text-field v-model=" writer" label="작성자" disabled></v-text-field>
        <v-btn :disabled="!valid" color="success" class="mr-4 btn" 
          @click="index !== undefined ? update() : write()">{{index !== undefined ? '수정' : '작성'}}
          <i class="fas fa-check-circle ml-1"></i></v-btn>
        <v-btn color="error" class="btn" @click="index !== undefined ? updatecancel() : addcancel()">취소
          <i class="fas fa-times-circle ml-1"></i>
        </v-btn>
      </v-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
// import data from '@/views/Notice/data'

export default {
  name: 'notice-create',
  data() {
    const index = this.$route.params.noticeId
    return {
      noticeData: [],
      index: index,
      // select: index !== undefined ? noticeData[index].category : null,
      // title: index !== undefined ? noticeData[index].title : "",
      // content: index !== undefined ? noticeData[index].content : "",
      // writer: index !== undefined ? noticeData[index].writer : "",
      valid: false,
      categoryRules: [[v => !!v || '분류를 선택해주세요']],
      titleRules: [
        v => !!v || '제목을 작성해주세요',
        v => (v && v.length <= 30) || '제목을 30자 이내로 작성해주세요',
      ],
      contentRules: [v => !!v || '내용을 작성해주세요'],
      createddate: "",
      categorys: [
        '일반',
        '중요',
        '테마',
        '장소',
      ]
    }
  },
  methods: {
    write() {
      var noticeCreateForms = {
        'category': this.select,
        'title': this.title,
        'content': this.content,
        'writer': this.writer,
        'writed_at': this.createddate,    
      }
      axios.post('/articles/theme_notice/', noticeCreateForms)
        .then(
          this.$router.push({
            path: '/notice'
          })
        )
        .catch(err => {
          console.log(err)
        })
    },
    update() {
      var noticeUpdateForms = {
        'category': this.select,
        'title': this.title,
        'content': this.content
      }
      axios.put(`/articles/theme_notice/${this.index}`, noticeUpdateForms)
        .then(
          this.$router.push({
            path: `/notice/detail/${this.index}`
          })
        )
        .catch(err => {
          console.log(err)
        })
    },
    reset () {
      this.$refs.form.reset()
    },
    addcancel () {
      this.$router.push({
        path: '/notice'
      })
    },
    updatecancel () {
      this.$router.push({
        path: `/notice/detail/${this.index}`
      })
    }
  },
  mounted() {
    axios.get(`/articles/notice/${this.index}/`)
      .then(response => {
        this.noticeData = response.data['notice']
      })
  }
}
</script>

<style scoped>
#notice-create {
  margin: 64px auto 0 auto;
  padding: 16px 0 60px 0;
  width: 100%;
  background-color: rgb(238, 240, 247);
}

.notice-title {
  font-family: 'Cafe24Simplehae';
  font-size: 40px;
  margin: 16px auto 0 auto;
  width: 50%;
  border-radius: 7px 7px 0 0;
  box-shadow: 1px 1px 2px 1px rgb(100, 105, 109);
  background-color: rgb(255, 255, 255);
  padding: 2rem 0;
}

.notice-body {
  background-color: #fff;
  width: 50%;
  padding: 1.2rem 2rem;
  margin: 0 auto 0 auto;
  border-radius: 0 0 7px 7px;
  box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
}

.reset {
  text-align: right;
}

.btn {
  font-family: 'Cafe24Simplehae';
  font-size: 18px;
}

.notice-create-form {
  padding: 2rem;
}

@media (max-width: 600px) {
  .notice-title {
    width: 95%;
  }
  .notice-body {
    width: 95%;
  }
  .notice-create-form {
    padding: 8px;
  }
}
</style>
