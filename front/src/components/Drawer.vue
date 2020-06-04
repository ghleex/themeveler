<template>
  <div id="drawer">
    <v-navigation-drawer
      v-model="drawer" :color="color" :expand-on-hover="expandOnHover" :mini-variant.sync="miniVariant"
      :right="false" :permanent="true" :src="bg" absolute dark
    >
      <v-list dense nav class="py-0">
        <v-list-item two-line :class="miniVariant && 'px-0'">
          <v-list-item-avatar>
            <h2><i class="fas fa-user-circle"></i></h2>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>{{ username() }}님</v-list-item-title>
            <v-list-item-subtitle>{{ userrole() }}</v-list-item-subtitle>
          </v-list-item-content>
          <v-btn icon @click.stop="miniVariant = !miniVariant" v-if="this.innerWidth < 600">
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
        </v-list-item>
        <v-divider></v-divider>

        <v-list-item v-for="item in items" :key="item.title" link :to="item.path" class="list-item">
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
export default {
  data () {
    return {
      drawer: true,
      items: [
        { title: '마이페이지', icon: 'mdi-view-dashboard', path: "/profiles" },
        { title: '비밀번호변경', icon: 'mdi-account-edit', path: "/editpassword" },
        { title: '회원정보수정', icon: 'mdi-account-edit', path: "/editprofile" },
        { title: '댓글 활동', icon: 'mdi-comment-text', path: "/profile/comment" },
        // { title: '미정..', icon: 'mdi-image', path: "/profiletest" },
      ],
      color: "primary",
      miniVariant: false,
      // miniVariant: window.innerWidth >= 600 ? false : true,
      expandOnHover: false,
      background: true,
      innerWidth: window.innerWidth
    }
  },
  methods: {
    winWidth() {
      if (window.innerWidth < 600) {
        this.miniVariant = true
      }
      else {
        this.miniVariant = false
      }
    },
    username() {
      return this.$session.get("nickname")
    },
    userrole() {
      if (this.$session.get("staff") === true) {
        return "관리자"
      }
      else {
        return "사용자"
      }
    }
  },
  mounted() {
    this.winWidth()
  },
  computed: {
    bg () {
      return this.background ? "https://cdn.vuetifyjs.com/images/backgrounds/bg-2.jpg" : undefined
    },
  }
}
</script>

<style scoped>
  .list-item:hover {
    text-decoration: none;
  }
</style>
