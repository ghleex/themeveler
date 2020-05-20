<template>
  <v-navigation-drawer
    v-model="drawer"
    :color="color"
    :expand-on-hover="expandOnHover"
    :mini-variant.sync="miniVariant"
    :right="false"
    :permanent="true"
    :src="bg"
    absolute
    dark
  >
    <v-list dense nav class="py-0">
      <v-list-item two-line :class="miniVariant && 'px-0'">
        <v-list-item-avatar>
          <h2><i class="fas fa-user-circle"></i></h2>
          <!-- <img src="https://randomuser.me/api/portraits/men/81.jpg"> -->
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>OOO님</v-list-item-title>
          <v-list-item-subtitle>user</v-list-item-subtitle>
        </v-list-item-content>

        <v-btn icon @click.stop="miniVariant = !miniVariant">
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
</template>

<script>
export default {
  data () {
    return {
      drawer: true,
      items: [
        { title: '마이페이지', icon: 'mdi-view-dashboard', path: "/profile" },
        { title: '회원정보수정', icon: 'mdi-help-box', path: "/editprofile" },
        { title: '댓글 관리', icon: 'mdi-image', path: "/profile/comment" },
        { title: '미정', icon: 'mdi-image', path: "/profiletest" },
      ],
      color: "primary",
      miniVariant: false,
      expandOnHover: false,
      background: true,
    }
  },
  computed: {
    bg () {
      return this.background ? 'https://cdn.vuetifyjs.com/images/backgrounds/bg-2.jpg' : undefined
    },
  },
}
</script>

<style scoped>
  .list-item:hover {
    text-decoration: none;
  }
</style>
