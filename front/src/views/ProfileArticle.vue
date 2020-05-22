<template>
  <v-app id="profile-article">
    <Drawer class="drawer" />

    <div class="comment">
      <v-data-table :headers="headers" :items="commentData" :page.sync="page" :items-per-page="itemsPerPage"
        hide-default-footer class="elevation-1" @page-count="pageCount = $event" :search="search"
        :sort-by="['id']" :sort-desc="true" dense>
        <template v-slot:top>
          <v-toolbar flat color="white">
            <h5 class="card-title">내가 작성한 글
              <v-chip class="ma-2 px-2" small color="orange" text-color="white">{{ commentCount }}</v-chip>
              <!-- <v-badge color="blue" content="5" inline="true"></v-badge> -->
            </h5>
            <v-spacer></v-spacer>
            <!-- 검색바 -->
            <div>
              <v-text-field v-model="search" append-icon="mdi-magnify" label="검색"
                single-line hide-details class="searchbar"></v-text-field>
            </div>
          </v-toolbar>
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
    </div>
  </v-app>
</template>

<script>
import Drawer from '../components/Drawer.vue'
import data from '@/views/Notice/data'

export default {
  name: 'ProfileArticle',
  components: {
    Drawer
  },
  data() {
    return {
      items: [
        { id: 1, icon: 'mdi-heart-outline', iconClass: 'orange lighten-1 white--text', title: '경복궁', subtitle: 'Jan 9, 2020' },
        { id: 2, icon: 'mdi-heart-outline', iconClass: 'purple lighten-1 white--text', title: '창경궁', subtitle: 'Jan 17, 2020' },
        { id: 3, icon: 'mdi-heart', iconClass: 'red lighten-1 white--text', title: '명동', subtitle: 'Jan 28, 2020' },
        { id: 4, icon: 'mdi-heart', iconClass: 'blue white--text', title: '인사동', subtitle: 'Jan 28, 2020' },
        { id: 5, icon: 'mdi-heart', iconClass: 'amber white--text', title: '청계천', subtitle: 'Jan 28, 2020' },
      ],
      page: 1,
      pageCount: 0,
      itemsPerPage: 20,
      search: '',
      headers: [
        { text: '번호', align: 'start', value: 'id', sortable: false },
        { text: '작성위치', value: 'category' },
        { text: '글내용', value: 'title', sortable: false },
        { text: '등록일', value: 'createddate', sortable: false }
      ],
      commentData: data,
      commentCount: data.length
      // commentCount: data.filter(val => val.content).length
    }
  },
  methods: {
    detail(id) {
      this.$router.push({
        name: 'notice-detail',
        params: {
          noticeId: id
        }
      })
    }
  }
}
</script>

<style scoped>
#profile-article {
  margin-top: 64px;
}

#profile-content {
  margin-left: 256px;
  width: 80%;
}

@media (max-width: 600px) {
  #profile-content {
    margin-left: 56px;
    width: 80%;
  }
  .comment {
    margin-left: 64px !important;
    width: 75% !important;
  }
  .searchbar {
    width: 70% !important;
  }
}

.content-title {
  text-align: left;
  margin-left: 20px;
  margin-top: 8px;
}

.content-body {
  margin-left: 2px;
  margin-right: 2px;
}

.card-title {
  margin-top: 8px;
  margin-bottom: 8px;
}

.comment {
  margin-top: 8px;
  margin-bottom: 80px;
  margin-left: 264px;
  margin-right: auto;
  text-align: center;
  width: 80%;
}

.searchbar {
  margin-left: auto;
  margin-right: auto;
  width: 80%;
}
</style>
