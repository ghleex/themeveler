<template>
  <v-toolbar color="rgba(255, 255, 255, 0.85)" class="search-box">
    <form class="search-form" @submit.prevent="searching()">
      <v-icon>mdi-magnify</v-icon>
      <v-autocomplete color="#4DD0E1" v-model="query" :loading="loading" :search-input.sync="search" cache-items
        class="form-input mx-4" flat hide-no-data hide-details label="Where do you want to go?" solo-inverted
        >
        <!-- type="text" -->
      </v-autocomplete>
      <v-btn color="#2c3e50" class="text-light mt-1" type="submit">검색</v-btn>
    </form>
  </v-toolbar>
</template>

<script>
  import axios from 'axios'

  export default {
    name: "searchbar",
    data() {
      return {
        query: null,
        search: "",
        searchResult: [],
        select: null,
        loading: false,
        items: [],
        states: [], // 모든 theme와, destination을 넣어줄 것
      }
    },
    watch: {
      search(val) {
        val && val !== this.query && this.querySelections(val)
      },
    },
    methods: {
      querySelections(v) {
        this.loading = true
        // Simulated ajax query

        setTimeout(() => {
          this.items = this.states.filter(e => {
            return (e || '').toLowerCase().indexOf((v || '').toLowerCase()) > -1
          })
          this.loading = false
        }, 500)
      },
      searching() {
        this.$router.push(`/searchresult?q=${this.search}`)
      }
    },
    mounted() {
      // all_theme name 담기
      const requestHeader = this.$store.getters.requestHeader
      axios.get('/travels/all_theme/', requestHeader)
        .then(response => {
          var theme = response.data.all_theme
          for (var i = 0; i < theme.length; i++) {
            this.states.push(theme[i].name);
          }
          console.log(this.states)
        })
      
      // all_destination name 담기
    }
  }
</script>

<style>
  .search-box {
    /* width: 50%; */
    border-radius: 20px;
  }

  .search-box .theme--light.v-text-field--solo-inverted.v-input--is-focused>.v-input__control>.v-input__slot {
    /* background: #4242426b; */
    background: #2c3e50;
  }

  .search-form {
    display: flex;
  }
</style>