<template>
  <div id="notice-create">
    <h4>공지사항 작성</h4>
    <div class="reset">
      <v-btn color="warning" @click="reset">다시 작성</v-btn>
    </div>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-select v-model="select" :items="categorys" :rules="categoryRules" label="분류" required></v-select>
      <v-text-field v-model="title" :counter="30" :rules="titleRules" label="제목" required></v-text-field>
      <v-text-field v-model="content" :rules="contentRules" label="내용" required></v-text-field>
      <v-text-field v-model=" writer" label="작성자" required></v-text-field>
      <v-btn :disabled="!valid" color="success" class="mr-4" 
        @click="index !== undefined ? update() : write()">{{index !== undefined ? '수정' : '작성'}}</v-btn>
      <v-btn color="error" @click="index !== undefined ? updatecancel() : addcancel()">취소</v-btn>
    </v-form>
    <!-- <button @click="index !== undefined ? update() : write()">{{index !== undefined ? '수정' : '작성'}}</button> -->
  </div>
</template>

<script>
import data from '@/views/Notice/data'

export default {
  name: 'notice-create',
  data() {
    const index = this.$route.params.noticeId;
    return {
      data: data,
      index: index,
      select: index !== undefined ? data[index].category : null,
      title: index !== undefined ? data[index].title : "",
      content: index !== undefined ? data[index].content : "",
      writer: index !== undefined ? data[index].writer : "",
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
      this.data.push({
        category: this.select,
        title: this.title,
        content: this.content,
        writer: this.writer
      })
      this.$router.push({
        path: '/notice'
      })
    },
    update() {
      data[this.index].category = this.select
      data[this.index].title = this.title
      data[this.index].content = this.content
      data[this.index].writer = this.writer
      this.$router.push({
        path: '/notice/detail/'+this.index
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
        path: '/notice/detail/'+this.index
      })
    }
  }
}
</script>

<style scoped>
#notice-create {
  margin-top: 80px;
  margin-bottom: 60px;
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}
#notice-create > h4 {
  text-align: left;
}
.reset {
  text-align: right;
}
</style>
