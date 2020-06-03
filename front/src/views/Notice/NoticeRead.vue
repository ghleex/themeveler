<template>
  <div id="notice-read">
    <div class="notice-title"><i class="fas fa-exclamation-circle mr-3"></i>공지사항</div>
    <div class="notice-body">
      <!-- 공지사항 리스트 Data table -->
      <v-data-table
        :headers="headers" :items="noticeData" :page.sync="page" :items-per-page="itemsPerPage" hide-default-footer
        class="notice-datatable" @page-count="pageCount = $event" :search="search" :sort-by="['id']" :sort-desc="true"
        style="white-space: nowrap" :calculate-widths="true"
      >
        <template v-slot:top>
          <v-toolbar class="notice-table-header" flat color="white">
            <v-toolbar-title></v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn color="#607D8B" dark class="mb-2" @click="write">글쓰기</v-btn>
          </v-toolbar>
        </template>
        <!-- 카테고리 색상 -->
        <template v-slot:item.category="{ item }">
          <v-chip :color="getColor(item.category)" dark>{{ item.category }}</v-chip>
        </template>
        <!-- 리스트 제목 -->
        <template v-slot:item.title="{ item }">
          <div class="notice-table-body" @click="detail(item.id)">{{ item.title }}</div>
        </template>
        <!-- 데이터가 없을 경우 -->
        <template slot="no-data">작성된 글이 없습니다</template>
      </v-data-table>
      <!-- 페이지 번호 -->
      <div class="text-center pt-2">
        <v-pagination v-model="page" :length="pageCount" color="#607D8B"></v-pagination>
      </div>
      <!-- 검색바 -->
      <div>
        <v-text-field v-model="search" append-icon="mdi-magnify" label="검색" single-line hide-details
          class="searchbar"></v-text-field>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "notice-read",
  data() {
    return {
      page: 1,
      pageCount: 0,
      itemsPerPage: 10,
      search: "",
      headers: [
        { text: "번호", align: "start", value: "id", sortable: false },
        { text: "분류", value: "category" },
        { text: "제목", value: "title", sortable: false },
        { text: "작성자", value: "writer_nickname", sortable: false },
        { text: "등록일", value: "writed_at" }
      ],
      noticeData: [],
      category: []
    }
  },
  methods: {
    write() {
      this.$router.push({
        path: '/notice/create'
      })
    },
    detail(noticeId) {
      this.$router.push({
        path: `/notice/detail/${noticeId}`
      })
    },
    getColor(category) {
      if (category == "중요") return "blue"
      else if (category == "일반") return "dark"
      else return "green"
    }
  },
  mounted() {
    axios.get('/articles/notices/')
      .then(response => {
        console.log(response.data)
        this.noticeData = response.data["notice"]
      })
      .catch(err => {
        console.log(err)
      })
    const requestHeader = this.$store.getters.requestHeader
    axios.get('/articles/n_category/', requestHeader)
      .then(response => {
        console.log(response.data)
        this.category = response.data["data"]
      })
      .catch(err => {
        console.log(err)
      })
  }
}
</script>

<style scoped>
  #notice-read {
    margin: 64px auto 0 auto;
    padding: 32px 0 48px 0;
    width: 100%;
    height: 100%;
    background-color: rgb(238, 240, 247);
  }

  .searchbar {
    margin: 24px auto;
    width: 30%;
  }

  .notice-title {
    font-family: 'Cafe24Simplehae';
    font-size: 40px;
    margin: 0 auto 0 auto;
    width: 80%;
    border-radius: 7px 7px 0 0;
    box-shadow: 1px 1px 2px 1px rgb(100, 105, 109);
    background-color: rgb(255, 255, 255);
    padding: 2rem 0;
  }

  .notice-body {
    background-color: #fff;
    width: 80%;
    padding: 1.2rem 2rem;
    margin: 0 10% 0 10%;
    border-radius: 0 0 7px 7px;
    box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
  }

  @media (max-width: 600px) {
    .notice-title {
      width: 95% !important;
    }
    .notice-body {
      width: 95% !important;
      margin: 0 auto !important;
    }
  }

  .notice-table-header {
    padding-bottom: 5rem;
  }

  .notice-table-body {
    width: 100%;
    height: 1.2rem;
    white-space: normal;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: pointer;
    word-wrap: break-word; 
    display: -webkit-box; 
    -webkit-line-clamp: 1; 
    -webkit-box-orient: vertical;
  }
</style>
