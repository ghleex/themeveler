<template>
  <div id="service-read">
    <div class="service-center-title"><i class="fas fa-exclamation-circle mr-3"></i>고객센터</div>
    <div class="service-body">
      <!-- 고객센터 리스트 Data table -->
      <v-data-table
        :headers="headers" :items="serviceData" :page.sync="page" :items-per-page="itemsPerPage" hide-default-footer
        class="service-dataTable" @page-count="pageCount = $event" :search="search" :sort-by="['id']" :sort-desc="true"
        style="white-space: nowrap" :calculate-widths="true"
      >
        <template v-slot:top>
          <v-toolbar class="service-table-header" flat color="white">
            <v-toolbar-title></v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn color="#607D8B" dark class="mb-2" @click="write">글쓰기</v-btn>
          </v-toolbar>
        </template>
        <!-- 카테고리 색상 -->
        <template v-slot:item.category_name="{ item }">
          <v-chip :color="getColor(item.category_name)" dark>{{ item.category_name }}</v-chip>
        </template>
        <!-- 리스트 제목 -->
        <template v-slot:item.title="{ item }">
          <div class="service-list-body" @click="detail(item.id)">{{ item.title }}</div>
        </template>
        <!-- 관리자 처리 -->
        <template v-slot:item.is_fixed="{ item }">
          <div v-if="item.is_fixed === false">미처리</div>
          <div v-else>답변완료</div>
        </template>
        <!-- 등록일 시간형식 -->
        <template v-slot:item.created_at="{ item }">
          <div>{{ item.created_at | moment("YYYY-MM-DD LT") }}</div>
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
          class="searchbar" color="#607D8B"></v-text-field>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "service-read",
  data() {
    return {
      page: 1,
      pageCount: 0,
      itemsPerPage: 5,
      search: "",
      headers: [
        { text: "번호", value: "id", sortable: false },
        { text: "분류", value: "category_name" },
        { text: "제목", value: "title", sortable: false },
        { text: "처리상태", value: "is_fixed", sortable: false },
        { text: "작성자", value: "request_user_nickname", sortable: false },
        { text: "등록일", value: "created_at" }
      ],
      serviceData: [],
      userId: ""
    }
  },
  methods: {
    write() {
      this.$router.push({
        path: '/service/create'
      })
    },
    detail(serviceId) {
      this.$router.push({
        path: `/service/detail/${serviceId}`
      })
    },
    getColor(category) {
      if (category == "테마") return "#FF5252"
      else if (category == "장소") return "dark"
      else return "#BA68C8"
    }
  },
  mounted() {
    this.userId = this.$store.getters.user_id
    const requestHeader = this.$store.getters.requestHeader
    axios.get(`/articles/customer/${this.userId}/`, requestHeader)
      .then(response => {
        this.serviceData = response.data
      })
      .catch(err => {
        console.log(err)
      })
  }
}
</script>

<style scoped>
  #service-read {
    margin: 64px auto 0 auto;
    padding: 32px 0 48px 0;
    width: 100%;
    height: 100%;
    background-color: rgb(238, 240, 247);
  }

  #service-read .searchbar {
    margin: 1.5rem auto;
    width: 30%;
  }

  #service-read .service-center-title {
    font-family: 'Cafe24Simplehae';
    font-size: 40px;
    margin: 0 auto 0 auto;
    width: 80%;
    border-radius: 7px 7px 0 0;
    box-shadow: 1px 1px 2px 1px rgb(100, 105, 109);
    background-color: rgb(255, 255, 255);
    padding: 2rem 0;
  }

  .service-list-body {
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

  @media (max-width: 600px) {
    .service-center-title {
      width: 95% !important;
    }
    
    .service-body {
      width: 95% !important;
      margin: 0 auto !important;
    }
  }
  
  #service-read .service-body {
    background-color: #fff;
    width: 80%;
    padding: 1.2rem 2rem;
    margin: 0 10% 0 10%;
    border-radius: 0 0 7px 7px;
    box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
  }
</style>
