<template>   
  <div id="app">
    <Navbar />
    <Home />
    <!-- <router-view></router-view> -->
    <!-- <router-view :key="$route.fullPath" /> -->
    <Footer />
  </div>
</template>

<script>
// import axios from 'axios'
import Navbar from './components/Navbar.vue'
import Home from './views/Home.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    Navbar, 
    Home,
    Footer
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>
