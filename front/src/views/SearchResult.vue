<template>
  <div id="search-result">
    <div class="container">
      <div class="search-result-banner">
        <div>
          <v-img class="mr-5" src="../assets/navlogo.png" width="15vw"></v-img>
        </div>
        <div class="search-result-banner-text" style="font-size: 8vw">
          Themeveler
        </div>
      </div>
      <div class="search-result-header">
        <SearchBar class="sresult-search-bar mx-auto my-3 pb-4" />
      </div>
    </div>
    <div class="result-search-content">
      <h5 class="sresult-header-text my-4 mx-8"><b style="font-size: 25px;">"{{ $route.query.q }}"</b> 에 대한 검색결과 ({{ themeData.length+placeData.length }} 개)</h5>
      <div class="container border search-result-container">
        <div class="theme-container" v-if="themeData.length !== 0">
          <p class="sresult-type"><i class="fas fa-search-location mr-2"></i>테마 검색결과</p>
          <li v-for="theme in themeData" :key="theme.id" @click="goThemePage(theme.id)">{{ theme.name }}</li>
        </div>
        <div class="place-container" style="border: 0;" v-if="placeData.length !== 0">
          <v-divider></v-divider>
          <p class="sresult-type"><i class="fas fa-search-location mr-2"></i>장소 검색결과</p>
          <li v-for="place in placeData" :key="place.id" @click="goPlacePage(place.themes[0])">{{ place.name }}</li>
        </div>
        <div v-if="themeData.length+placeData.length === 0">일치하는 검색결과가 없습니다.</div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from "axios"
  import SearchBar from "@/components/SearchBar.vue"

  export default {
    name: "SearchResult",
    components: {
      SearchBar
    },
    data() {
      return {
        themeData: [],
        placeData: []
      }
    },
    methods: {
      goThemePage(themeId) {
        this.$router.push({
          path: `/travel/${themeId}`
        })
      },
      goPlacePage(themeId) {
        this.$router.push({
          path: `/travel/${themeId}`
        })
      },
      searchNow(query) {
        axios.get(`/articles/search/${query}/`)
          .then(response => {
            this.themeData = response.data.theme
            this.placeData = response.data.dest
          })
          .catch(err => {
            console.log(err)
          })
      }
    },
    watch: {
      keyword() {
        this.searchNow(this.keyword)
      }
    },
    computed: {
      keyword() {
        return this.$route.query.q
      }
    },
    mounted() {
      this.searchNow(this.$route.query.q)
    }
  }
</script>

<style>
  #search-result {
    margin-top: 64px;
    padding-top: 16px;
    background-color: #ECEFF1;
    height: 100%;
  }

  .search-result-banner {
    display: flex;
    margin: 20px auto 48px auto;
    justify-content: center;
    align-items: center;
  }

  .search-result-banner-text {
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: 700;
    font-family: "Cafe24Simplehae";
    font-style: italic;
    font-size: 70px;
  }

  .result-search-content {
    /* background-color: #2c3e50; */
    width: 90vw;
    margin: 2rem auto 5rem auto;
    padding: .5rem 1rem;
    border-radius: 5px;
  }

  .search-result-container {
    background-color: #fff;
  }

  .sresult-header-text {
    font-family: "Cafe24Simplehae";
    text-align: left;
    margin:0 24px;
    border-bottom: 1px solid;
    padding-bottom: .5rem;
  }

  .theme-container,
  .place-container {
    text-align: left;
  }

  .theme-container > li,
  .place-container > li {
    padding: .5rem;
  }

  .theme-container > li:hover,
  .place-container > li:hover {
    background-color: rgba(52, 41, 95, 0.05);
    cursor: pointer;
    font-weight: bold;
  }

  .sresult-type {
    font-family: "Cafe24Simplehae";
    font-size: 25px;
  }

  .sresult-search-bar .search-form {
    width: 100%;
  }
</style>
