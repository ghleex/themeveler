<template>
  <div id="service-read">
    <div class="service-center-title">
      <i class="fas fa-exclamation-circle"></i> 고객센터
    </div>
    <!-- 공지사항 리스트 Data table -->
    <div class="service-body">
      <v-data-table
        :headers="headers" :items="data" :page.sync="page" :items-per-page="itemsPerPage" hide-default-footer
        class="service-dataTable" @page-count="pageCount = $event" :search="search" :sort-by="['id']" :sort-desc="[true]"
        style="white-space: nowrap" :calculate-widths="true"
      >
        <template v-slot:top>
          <v-toolbar class="service-center-header" flat color="white">
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
          <div class="service-list-body" @click="detail(item.id)">{{ item.title }}</div>
        </template>
        <!-- data가 없을 시 -->
        <template slot="no-data">
          <v-alert :value="true" color="error" icon="warning">
            Sorry, nothing to display here :(
          </v-alert>
        </template>
      </v-data-table>
      <!-- 페이지 번호 -->
      <div class="text-center pt-2">
        <v-pagination color="#607D8B" v-model="page" :length="pageCount"></v-pagination>
      </div>
      <!-- 검색바 -->
      <div>
        <v-text-field color="#607D8B" v-model="search" append-icon="mdi-magnify" label="검색" single-line hide-details class="searchbar">
        </v-text-field>
      </div>
    </div>
  </div>
</template>

<script>
  import data from '@/views/ServiceCenter/data'

  export default {
    name: 'service-read',
    data() {
      return {
        page: 1,
        pageCount: 0,
        itemsPerPage: 5,
        search: '',
        headers: [{
            text: '번호',
            value: 'id',
            sortable: false,
          },
          {
            text: '분류',
            value: 'category',
          },
          {
            text: '제목',
            value: 'title',
            sortable: false,
            // width: 100
          },
          {
            text: '작성자',
            value: 'writer',
            sortable: false,
          },
          {
            text: '등록일',
            value: 'createddate',
          }
        ],
        data: data
      }
    },
    methods: {
      write() {
        this.$router.push({
          path: '/service/create'
        })
      },
      detail(id) {
        this.$router.push({
          name: 'service-detail',
          params: {
            serviceId: id
          }
        })
      },
      getColor(category) {
        if (category == '신고') return '#FF5252'
        else if (category == '건의') return 'dark'
        else return '#BA68C8'
      },
    },
  }
</script>

<style scoped>
  #service-read {
    margin: 64px auto 0 auto;
    width: 100%;
    background-color: rgb(238, 240, 247);
  }

  #service-read .searchbar {
    margin: 1.5rem auto;
    width: 30%;
  }

  #service-read .service-center-title {
    font-family: 'Cafe24Simplehae';
    font-size: 40px;
    margin: 5rem auto 0 auto;
    /* background-color: rgb(255, 187, 0); */
    width: 80%;
    border-radius: 7px 7px 0 0;
    box-shadow: 1px 1px 2px 1px rgb(100, 105, 109);
    background-color: rgb(255, 255, 255);
    padding: 2rem 0;
  }

  .service-center-header {
    padding-bottom: 5rem;
  }

  .service-dataTable {
    /* white-space: nowrap; */
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
    margin: 0 10% 5rem 10%;
    border-radius: 0 0 7px 7px;
    box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
  }
</style>
