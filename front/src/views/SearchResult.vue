<template>
  <div id="search-result">
    <div class="container">
      <div class="sresultheader">
        <h4 class="my-3">"{{ $route.query.q }}" 에 대한 검색결과 ({{ spotData.length }} 개)</h4>
        <SearchBar class="sresult-search-bar mx-auto my-3 pb-4" />
      </div>
    </div>
    <div class="container border">
      <div class="spot-container">
        <spot-list spotData="spotData" />
      </div>

      <div class="theme-container">
        <theme-list :themeData="themeData" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"
import SearchBar from '../components/SearchBar.vue'
// import ThemeList from "../components/ThemeList.vue"
// import SpotList from "../components/SpotList.vue"

export default {
  name: "SearchResult",
  components: {
    SearchBar,
    // SpotList,
    // ThemeList
  },
  data() {
    return {
			spotData: [],
			themeData: []
		};
  },
  methods: {
    goToSpotPage(spot_id) {
      axios.get(`/spot/${spot_id}/`)
        .then(response => {
          console.log(response);
        })
        .catch(error => {
          console.log(error.response);
        })
		},
    searchNow(query) {
      axios.get(`/search/${query}/`)
        .then(response => {
					this.spotData = response.data.spots
					this.themeData = response.data.themes
        })
    }
	},
	mounted() {
		let queries = this.$route.query.q.split(' ')
		this.searchNow(queries.join('|'))
	}
}
</script>

<style>
.sresultheader {
  margin-top: 60px;
  background: #11A0DC;
  border-radius: 10px 10px 0 0;
  border: 1px solid lightgray;  
}
.sresult-search-bar {
  width: 75%;
}
</style>
