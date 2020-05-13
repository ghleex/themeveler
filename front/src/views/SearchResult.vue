<template>
  <div id="search-result">
    <div class="container">
      <div class="sresultheader">
        <h3>"{{ $route.query.q }}" 에 대해 검색하여</h3>
        <h4>{{ cafeData.length }} 개의 결과를 찾았습니다</h4>
        <SearchBar class="mx-auto my-3 pb-4" />
      </div>
    </div>
    <div class="container border">
      <div class="spot-container">
        <review-list spotData="spotData" />
      </div>

      <div class="theme-container">
        <cafe-list :themeData="themeData" />
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
      axios
        .get(`${this.$store.state.constants.SERVER}/spot/${spot_id}`)
        .then(response => {
          console.log(response);
        })
        .catch(error => {
          console.log(error.response);
        });
		},
    searchNow(query) {
      axios
        .get(`${this.$store.state.constants.SERVER}/search/${query}`)
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
  background: #89B0AE;
  border-radius: 10px 10px 0 0;
  border: 1px solid lightgray;  
}
</style>
