<template>
  <div id="notice-read">
    <!-- 공지사항 리스트 Data table -->
    <v-data-table
      :headers="headers"
      :items="data"
      :page.sync="page"
      :items-per-page="itemsPerPage"
      hide-default-footer
      class="elevation-1"
      @page-count="pageCount = $event"
      :search="search"
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title><h4>공지사항</h4></v-toolbar-title>
          <v-spacer></v-spacer>
          <!-- <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on }">
              <v-btn color="primary" dark class="mb-2" v-on="on">New Item</v-btn>
            </template>
          </v-dialog> -->
          <v-btn color="primary" dark class="mb-2" @click="write">글쓰기</v-btn>
        </v-toolbar>
      </template>
      <!-- 카테고리 색상 -->
      <template v-slot:item.category="{ item }">
        <v-chip :color="getColor(item.category)" dark>{{ item.category }}</v-chip>
      </template>
      <!-- 리스트 제목 -->
      <template v-slot:item.title="{ item }">
        <div @click="detail(item.id)">{{ item.title }}</div>
      </template>
    </v-data-table>
    <!-- 페이지 번호 -->
    <div class="text-center pt-2">
      <v-pagination v-model="page" :length="pageCount"></v-pagination>
    </div>
    <!-- 검색바 -->
    <div>
      <v-text-field v-model="search" append-icon="mdi-magnify" label="검색"
        single-line hide-details class="searchbar"></v-text-field>
    </div>
  </div>
</template>

<script>
import data from '@/views/Notice/data'

export default {
  name: 'notice-read',
  data() {
    return {
      page: 1,
      pageCount: 0,
      itemsPerPage: 10,
      search: '',
      headers: [
        { text: '번호', align: 'start', sortable: false, value: 'id' },
        { text: '분류', value: 'category' },
        { text: '제목', value: 'title' },
        { text: '작성자', value: 'writer', sortable: false },
        { text: '등록일', value: 'createddate' }
      ],
      data: data
    }
  },
  methods: {
    write() {
      this.$router.push({
        path: '/notice/create'
      })
    },
    detail(id) {
      this.$router.push({
        name: 'notice-detail',
        params: {
          noticeId: id
        }
      })
    },
    getColor(category) {
      if (category == '중요') return 'blue'
      else if (category == '일반') return 'dark'
      else return 'green'
    }
  }
}
</script>

<style scoped>
#notice-read {
  margin-top: 80px;
  margin-bottom: 60px;
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  width: 95%;
}
.searchbar {
  margin-left: auto;
  margin-right: auto;
  width: 30%;
}
</style>
