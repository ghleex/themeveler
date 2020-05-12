<template>
  <div class="container-fluid p-0">
    <nav-bar bgcolor="#FFD6AA" />
    <div id="app">
      <img alt="image01" width="70%" src="./assets/image/image01.jpg">
      <h3>점검 중입니다..</h3>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  components: {

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
  margin-top: 60px;
}
</style>
