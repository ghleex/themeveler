<template>
  <div id="notice-read">
    <v-data-table
      :headers="headers"
      :items="data"
      @click:row="detail(items.index())"
      :page.sync="page"
      :items-per-page="itemsPerPage"
      hide-default-footer
      class="elevation-1"
      @page-count="pageCount = $event"
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>공지사항</v-toolbar-title>
          <v-spacer></v-spacer>
          <!-- <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on }">
              <v-btn color="primary" dark class="mb-2" v-on="on">New Item</v-btn>
            </template>
          </v-dialog> -->
          <v-btn color="primary" dark class="mb-2" @click="write">글쓰기</v-btn>
        </v-toolbar>
      </template>
    </v-data-table>
    <div class="text-center pt-2">
      <v-pagination v-model="page" :length="pageCount"></v-pagination>
      <!-- <v-text-field
        :value="itemsPerPage"
        label="Items per page"
        type="number"
        min="-1"
        max="15"
        @input="itemsPerPage = parseInt($event, 10)"
      ></v-text-field> -->
      <!-- <button @click="write">글쓰기</button> -->
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
      headers: [
        { text: '번호', align: 'start', sortable: false, value: 'id' },
        { text: '분류', value: 'category' },
        { text: '제목', value: 'title' },
        { text: '작성자', value: 'writer', sortable: false },
        { text: '작성일자', value: 'createddate' },
        { text: '추천수', value: 'content' }
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
    detail(index) {
      this.$router.push({
        name: 'notice-detail',
        params: {
          contentId: index
        }
      })
    }
  }
}

</script>

<style scoped>
#notice-read {
  margin-top: 70px;
  margin-bottom: 60px;
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  width: 95%;
}
</style>
