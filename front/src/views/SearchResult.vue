<template>
  <div id="search-result">
    <div class="container">
      <div class="sresultheader">
        <SearchBar class="sresult-search-bar mx-auto my-3 pb-4" />
        <h5 class="sresult-header my-3">"{{ $route.query.q }}" 에 대한 검색결과 ({{ themeData.length+placeData.length }} 개)</h5>
      </div>
    </div>
    <div class="container border">
      <div class="theme-container" v-if="themeData">
        <!-- <theme-list :themeData="themeData" /> -->
        <p>테마 검색결과</p>
        <li v-for="theme in themeData" :key="theme.id" @click="goThemePage(theme.id)">{{ theme.name }}</li>
      </div>
      <div class="place-container" v-else-if="placeData">
        <!-- <place-list :placeData="placeData" /> -->
        <v-divider></v-divider>
        <p>장소 검색결과</p>
        <li v-for="place in placeData" :key="place.id">{{ place.name }}</li>
      </div>
      <div v-else>일치하는 검색결과가 없습니다.</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SearchBar from '@/components/SearchBar.vue'
// import ThemeList from "@/components/ThemeList.vue"
// import PlaceList from "@/components/PlaceList.vue"

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
    searchNow(query) {
      axios.get(`/articles/search/${query}/`)
        .then(response => {
          console.log(response.data)
					this.themeData = response.data.theme
          this.placeData = response.data.dest
        })
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

  .sresult-header {
    font-family: 'Cafe24Simplehae';
    text-align: left;
    margin-left: 24px;
  }

  .theme-container,
  .place-container {
    text-align: left;
  }
</style>
