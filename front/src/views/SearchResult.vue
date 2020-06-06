<template>
  <div id="search-result">
    <div class="container">
      <div class="sresultheader">
        <SearchBar class="sresult-search-bar mx-auto my-3 pb-4" />
        <h5 class="sresult-header-text my-3">"{{ $route.query.q }}" 에 대한 검색결과 ({{ themeData.length+placeData.length }} 개)</h5>
      </div>
    </div>
    <div class="container border">
      <div class="theme-container" v-if="themeData.length !== 0">
        <p class="sresult-type">테마 검색결과</p>
        <li v-for="theme in themeData" :key="theme.id" @click="goThemePage(theme.id)">{{ theme.name }}</li>
      </div>
      <div class="place-container" v-if="placeData.length !== 0">
        <v-divider></v-divider>
        <p class="sresult-type">장소 검색결과</p>
        <li v-for="place in placeData" :key="place.id" @click="goPlacePage(place.themes[0])">{{ place.name }}</li>
      </div>
      <div v-if="themeData.length+placeData.length === 0">일치하는 검색결과가 없습니다.</div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import SearchBar from '@/components/SearchBar.vue'

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
        this.$router.push(`/travel/${themeId}`)
      },
      goPlacePage(themeId) {
        this.$router.push(`/travel/${themeId}`)
      },
      searchNow(query) {
        axios.get(`/articles/search/${query}/`)
          .then(response => {
            this.themeData = response.data.theme
            this.placeData = response.data.dest
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
  }

  .sresultheader {
    background: #11A0DC;
    border-radius: 10px 10px 10px 10px;
    border: 1px solid lightgray;
  }

  .sresult-search-bar {
    width: 95%;
  }

  .sresult-header-text {
    font-family: 'Cafe24Simplehae';
    text-align: left;
    margin-left: 24px;
  }

  .theme-container,
  .place-container {
    text-align: left;
  }

  .sresult-type {
    font-family: 'Cafe24Simplehae';
    font-size: 18px;
  }
</style>
