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
        <v-list-item v-for="item in items" :key="item.title" link :to="item.path">
          <!-- <router-link :to="item.path"></router-link> -->
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
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" class="d-block d-md-none"></v-app-bar-nav-icon>
      <v-list-item-avatar class="mr-2 d-none d-md-block">
        <v-img
          src='https://user-images.githubusercontent.com/52684457/81582000-7606aa00-93ea-11ea-86e9-06324fd4b39c.png'>
        </v-img>
      </v-list-item-avatar>
      <v-toolbar-title>Themeveler</v-toolbar-title>

      <v-spacer></v-spacer>
      <v-toolbar-items class="d-none d-md-block">

        <v-btn text v-for="item in menuItems" :key="item.title" :to="item.path">

          <div class="drop-yes" v-if="item.title == 'Contact'">
            <v-icon class="mr-2">{{ item.icon }}</v-icon>
            {{ item.title }}
            <div class="dropdown-content">
              <a href="#" class="mt-3">공지사항</a>
              <hr>
              <a href="#" class="mb-3">고객센터</a>
            </div>
          </div>

          <div class="drop-no" v-else>
            <v-icon class="mr-2">{{ item.icon }}</v-icon>
            {{ item.title }}
          </div>

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
            icon: 'mdi-image-album'
          },
          {
            title: 'Contact',
            icon: 'mdi-account-supervisor-circle'
          },
          {
            title: 'Sign in',
            icon: 'mdi-login-variant',
            path: '/login'
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
            icon: 'mdi-login-variant',
            path: '/login'
          },
        ],
      }
    }
  }
</script>

<style lang="scss" scoped>
  .navbar_box>img {
    width: 100%;
  }
  
  .dropdown-content {
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    min-width: 140px;
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
    z-index: 1;
    left: -15px;
    top: 25px;
  }

    .drop-yes:hover .dropdown-content {
    display: block;
  }

  .dropdown-content a {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
  }

  .dropdown-content a:hover {background-color: #f1f1f1}


</style>

