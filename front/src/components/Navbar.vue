<template>
  <div class="navbar_box">

    <!-- 사이드바 -->
    <v-navigation-drawer v-model="drawer" absolute temporary>
      <v-list-item class="mt-2">
        <v-list-item-avatar>
          <v-img
            src='https://user-images.githubusercontent.com/52684457/81582000-7606aa00-93ea-11ea-86e9-06324fd4b39c.png'>
          </v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title class="ml-2"><b>Themeveler</b></v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense>
        <v-list-item v-for="item in items" :key="item.title" :to="item.path" link>
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="ml-2">{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!--  상단바 -->
    <!-- <v-toolbar flat extended extension-height="-64" color="primary"> -->
    <v-toolbar flat absolute width="100%" color="rgba(255, 255, 255, 0.8)">
      <!-- 메뉴를 click하면 사이드에 메뉴가 뜸 -->
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" class="d-none d-sm-block d-md-none"></v-app-bar-nav-icon>
      <v-list-item-avatar class="mr-2 d-sm-none d-md-block">
        <v-img
          src='https://user-images.githubusercontent.com/52684457/81582000-7606aa00-93ea-11ea-86e9-06324fd4b39c.png'>
        </v-img>
      </v-list-item-avatar>
      <v-toolbar-title>Themeveler</v-toolbar-title>

      <v-spacer></v-spacer>
      <v-toolbar-items class="d-sm-none d-md-block">
        <v-btn text v-for="item in menuItems" :key="item.title" :to="item.path">
          <v-icon class="mr-2">{{ item.icon }}</v-icon>
          {{ item.title }}
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
  </div>
</template>


<script>
  export default {
    name: 'Navbar',
    data() {
      return {
        drawer: null,
        menuItems: [{
            title: 'Home',
            icon: 'mdi-home',
            path: '/'
          },
          {
            title: 'Travel',
            icon: ' mdi-image-album'
          },
          {
            title: 'Contact',
            icon: 'mdi-account-supervisor-circle'
          },
          {
            title: 'Sign in',
            icon: 'mdi-login-variant'
          },
        ],
        items: [{
            title: 'Home',
            icon: 'mdi-home',
            path: '/'
          },
          {
            title: 'Travel',
            icon: ' mdi-image-album'
          },
          {
            title: 'Contact',
            icon: 'mdi-account-supervisor-circle'
          },
          {
            title: 'Sign in',
            icon: 'mdi-login-variant'
          },
        ],
      }
    },
  }
</script>

<style lang="scss" scoped>
  .navbar_box > img {
    width: 100%;
  }

</style>