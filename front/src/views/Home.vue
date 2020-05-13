<template>
  <div class="header">
    <div class="banner">
      <img src="https://user-images.githubusercontent.com/52684457/81634040-0d024f00-9449-11ea-9c87-a5212ec353e3.jpg"
        alt="">
    </div>
    <div class="home-search-bar">
      <SearchBar />
    </div>
  </div>
</template>

<script>
  import SearchBar from '../components/SearchBar'

  export default {
    components: {
      SearchBar,
    }
  }
</script>

<style scoped>
  .banner {
    position: relative;
    overflow: hidden;
    height: 500px;
  }

  .banner>img {
    width: 100%;
    /* max-height: initial; */
    margin-top: -15%;
  }

  .home-search-bar {
    position: absolute;
    top: 20vw;
    left: 50%;
    transform: translate(-50%, -50%);
  }
</style>