<template>   
  <div class="container-fluid p-0">
    <Navbar />
    <div id="app">
      <Home />
    </div>
  </div>
</template>

<script>
/// mport axios from 'axios'
import Navbar from './components/Navbar.vue'
import Home from './views/Home'

export default {
  name: 'App',
  components: {
    Navbar, 
    Home,
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