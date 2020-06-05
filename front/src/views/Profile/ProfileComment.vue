<template>
  <v-app id="profile-comment">
    <Drawer class="drawer" />

    <div class="comment">
      <div class="profile-comment-title">
        <h5 class="card-title">내가 작성한 댓글
          <v-chip class="ma-2 px-2" small color="orange" text-color="white">{{ commentCount }}</v-chip>
        </h5>
      </div>
      <v-divider></v-divider>
      <v-data-table :headers="headers" :items="commentData" :page.sync="page" :items-per-page="itemsPerPage"
        hide-default-footer class="elevation-1" @page-count="pageCount = $event" :sort-by="['id']" :sort-desc="true" dense>
        <template v-slot:top>
        </template>
        <!-- 리스트 제목 -->
        <template v-slot:item.title="{ item }">
          <div @click="detail(item.id)">{{ item.title }}</div>
        </template>
        <!-- 등록일 시간형식 -->
        <template v-slot:item.created_at="{ item }">
          <div>{{ item.created_at | moment("YYYY-MM-DD LT") }}</div>
        </template>
        <!-- 데이터가 없을 경우 -->
        <template slot="no-data">작성한 댓글이 없습니다</template>
      </v-data-table>
      <!-- 페이지 번호 -->
      <div class="text-center pt-2">
        <v-pagination v-model="page" :length="pageCount"></v-pagination>
      </div>
    </div>

    <div class="recomment">
      <div class="profile-recomment-title">
        <h5 class="re-card-title">내가 작성한 대댓글
          <v-chip class="ma-2 px-2" small color="orange" text-color="white">{{ reCommentCount }}</v-chip>
        </h5>
      </div>
      <v-divider></v-divider>
      <v-data-table :headers="headers_re" :items="reCommentData" :page.sync="page_re" :items-per-page="itemsPerPage_re"
        hide-default-footer class="elevation-1" @page-count="pageCount_re = $event" :sort-by="['id']" :sort-desc="true" dense>
        <template v-slot:top>
        </template>
        <!-- 리스트 제목 -->
        <template v-slot:item.title="{ item }">
          <div @click="redetail(item.id)">{{ item.title }}</div>
        </template>
        <!-- 등록일 시간형식 -->
        <template v-slot:item.created_at="{ item }">
          <div>{{ item.created_at | moment("YYYY-MM-DD LT") }}</div>
        </template>
        <!-- 데이터가 없을 경우 -->
        <template slot="no-data">작성한 대댓글이 없습니다</template>
      </v-data-table>
      <!-- 페이지 번호 -->
      <div class="text-center pt-2">
        <v-pagination v-model="page" :length="pageCount"></v-pagination>
      </div>
    </div>
  </v-app>
</template>

<script>
import axios from 'axios'
import Drawer from '@/components/Drawer.vue'

export default {
  name: "ProfileComment",
  components: {
    Drawer
  },
  data() {
    return {
      page: 1,
      pageCount: 0,
      itemsPerPage: 10,
      headers: [
        { text: "번호", value: "id", sortable: false },
        { text: "댓글 내용", value: "content", sortable: false },
        { text: "등록일", value: "created_at", sortable: false }
      ],
      commentData: [],
      commentCount: 0,
      page_re: 1,
      pageCount_re: 0,
      itemsPerPage_re: 10,
      headers_re: [
        { text: "번호", value: "id", sortable: false },
        { text: "댓글 내용", value: "content", sortable: false },
        { text: "등록일", value: "created_at", sortable: false }
      ],
      reCommentData: [],
      reCommentCount: 0,
      userId: ""
    }
  },
  methods: {
    detail(commentsId) {
      this.$router.push({
        path: `/articles/cv/${this.userId}/${commentsId}`
      })
    },
    redetail(reCommentsId) {
      this.$router.push({
        path: `/articles/cv/${this.userId}/${reCommentsId}`
      })
    }
  },
  mounted() {
    this.userId = this.$store.getters.user_id
    const requestHeader = this.$store.getters.requestHeader
    axios.get(`/articles/comment_self/${this.userId}/`, requestHeader)
      .then(response => {
        this.commentData = response.data
        this.commentCount = response.data.length
      })
      .catch(err => {
        console.log(err)
      })
    axios.get(`/articles/recomment/${this.userId}/`, requestHeader)
      .then(response => {
        this.reCommentData = response.data
        this.reCommentCount = response.data.length
      })
      .catch(err => {
        console.log(err)
      })
  }
}
</script>

<style scoped>
  #profile-comment {
    margin-top: 64px;
    background-color: rgba(245, 245, 245, 0.5);
  }

  .profile-comment-title {
    text-align: left;
    margin-left: 16px;
  }

  @media (max-width: 600px) {
    .comment {
      margin-left: 64px !important;
      width: 75% !important;
    }
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


  .profile-recomment-title {
    text-align: left;
    margin-left: 16px;
  }

  @media (max-width: 600px) {
    .recomment {
      margin-left: 64px !important;
      width: 75% !important;
    }
  }

  .re-card-title {
    margin-top: 8px;
    margin-bottom: 8px;
  }

  .recomment {
    margin-top: 8px;
    margin-bottom: 80px;
    margin-left: 264px;
    margin-right: auto;
    text-align: center;
    width: 80%;
  }
</style>
