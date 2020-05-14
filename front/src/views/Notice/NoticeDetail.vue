<template>
  <div id="notice-detail">
    <h4>공지사항 <a>{{data.id}}</a>번글</h4>
    <div>작성자: {{data.writer}}</div><br>
    <div>제목: {{data.title}}</div><br>
    <div>내용: {{data.content}}</div><br>
    <v-btn color="warning" class="mr-4" @click="updateData">수정</v-btn>
    <v-btn color="error" class="mr-4" @click="deleteData">삭제</v-btn>
    <v-btn color="primary" @click="back">목록</v-btn>
  </div>
</template>

<script>
import data from '@/views/Notice/data'

export default {
  name: 'notice-detail',
  data() {
    const index = this.$route.params.noticeId
    return {
      data: data[index],
      index: index
    }
  },
  methods: {
    deleteData() {
      data.splice(this.index, 1)
      this.$router.push({
        path: '/notice'
      })
    },
    updateData() {
      this.$router.push({
        name: 'notice-create',
        params: {
          noticeId: this.index
        }
      })
    },
    back() {
      this.$router.push({
        path: '/notice'
      })
    }
  }
}
</script>

<style scoped>
#notice-detail {
  margin-top: 80px;
  margin-bottom: 60px;
  width: 90%;
}
#notice-detail>h4 {
  text-align: center;
  margin-bottom: 20px;
}
#notice-detail>h4>a {
  color: goldenrod;
}
</style>
