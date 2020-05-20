<template>
  <div class="navbar_box">

    <!-- 사이드바 -->
    <v-navigation-drawer class="text-start sideBar-zIndex" v-model="drawer" absolute temporary>
      <v-list-item class="mt-2">
        <v-list-item-avatar>
          <v-img class="nav-avartar" src='../assets/navlogo.png'></v-img>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title><router-link to="/" class="text-dark"> <b>Themeveler</b></router-link></v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list>
        <v-list-item class="side-no-padding" color="#263238" v-for="item in items" :key="item.title" link :to="item.path">
          <!-- <router-link :to="item.path"></router-link> -->
          <template v-if="item.title != 'Contact'">
          <v-list-item-icon>
            <v-icon class="pl-4">{{ item.icon }}</v-icon>
          </v-list-item-icon>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </template>

          <v-list-group class="side-width-100" color="#263238" no-action value="true" v-else-if="item.title == 'Contact'">
            <template class="contact-custom" v-slot:activator>
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
              <!-- <v-list-item-content> -->
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              <!-- </v-list-item-content> -->
            </template>
              <v-list-item link>
                <v-list-item-title class="contact-list-group"><router-link to="/notice">공지사항</router-link></v-list-item-title>
              </v-list-item>
              <v-list-item link>
                <v-list-item-title class="contact-list-group"><router-link to="/service">고객센터</router-link></v-list-item-title>
              </v-list-item>
          </v-list-group>

        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!--  상단바 -->
    <!-- <v-toolbar flat extended extension-height="-64" color="primary"> -->
    <v-toolbar flat absolute width="100%" color="rgba(255, 255, 255, 0.8)">
      <!-- 메뉴를 click하면 사이드에 메뉴가 뜸 -->
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" class="d-block d-md-none"></v-app-bar-nav-icon>
      <v-list-item-avatar class="mr-2 d-none d-md-block">
        <v-img src='../assets/navlogo.png'></v-img>
      </v-list-item-avatar>
      <router-link to="/" class="navtitle">
        <v-toolbar-title>Themeveler</v-toolbar-title>
      </router-link>
      <v-spacer></v-spacer>
      <v-toolbar-items class="d-none d-md-block">

        <v-btn text v-for="item in menuItems" :key="item.title" :to="item.path">

          <div class="drop-yes" v-if="item.title == 'Contact'">
            <v-icon class="mr-2">{{ item.icon }}</v-icon>
            {{ item.title }}
            <div class="dropdown-content">
              <a href="/notice" class="mt-2">공지사항</a>
              <hr class="my-2">
              <a href="/service" class="mb-2">고객센터</a>
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
@media (max-width: 767px) {
  .navbar_box {
    // position: fixed;
  }
}

  .navbar_box>img {
    width: 100%;
  }

  .sideBar-zIndex {
    z-index: 20;
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

  .dropdown-content a:hover {
    background-color: #f1f1f1
  }

  .navtitle {
    color: black;
    text-decoration: none;
  }

  .nav-avartar {
    margin-right: 0 !important;
  }

  .navbar_box .v-list-item__icon {
    margin-right: 1rem !important;
  }

  .navbar_box {
    z-index: 15;
  }

  .navbar_box header {
    z-index: 15;
  }

  .drop-yes:hover {
    text-decoration: none;
  }

  .navbar_box .v-list-group__header {
    padding : 0 !important;
  }

  .contact-list-group > a {
    color: rgb(40, 40, 44);
  }

  .side-width-100 {
    width: 100%;
  }

  .side-no-padding {
    padding: 0;
  }

// ["role":"button"]

</style>