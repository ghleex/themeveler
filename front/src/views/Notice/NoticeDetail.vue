<template>
  <div id="notice-detail">
    <h4>공지사항 <a>{{data.id}}</a>번글</h4>
    <div>{{data.writer}}</div><br>
    <div>{{data.title}}</div><br>
    <div>{{data.content}}</div><br>
    <v-btn color="warning" class="mr-4" @click="updateData">수정</v-btn>
    <v-btn color="error" class="mr-4" @click="deleteData">삭제</v-btn>
    <v-btn color="primary" @click="deleteData">목록</v-btn>
  </div>
</template>

<script>
import data from '@/views/Notice/data'

export default {
  name: 'notice-detail',
  data() {
    const index = this.$route.params.contentId
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
          contentId: this.index
        }
      })
    }
  }
}
</script>
<style scoped>
#notice-detail {
  margin-top: 70px;
  margin-bottom: 60px;
  width: 90%;
}
#notice-detail>h4>a {
  color: goldenrod;
}
</style>
