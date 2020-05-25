<template>
<!-- https://codepen.io/pen/?&editable=true&editors=101=https%3A%2F%2Fvuetifyjs.com%2Fen%2Fcomponents%2Fautocompletes%2F -->
  <v-toolbar
    color="rgba(255, 255, 255, 0.85)"
    class="search-box"
  >
  <v-icon>mdi-magnify</v-icon>
    <!-- <v-toolbar-title class="d-none d-sm-none">Search</v-toolbar-title> -->
    <v-autocomplete
      v-model="select"
      :loading="loading"
      :items="items"
      :search-input.sync="search"
      cache-items
      class="mx-4"
      flat
      hide-no-data
      hide-details
      label="Where do you want to go?"
      solo-inverted
    ></v-autocomplete>
    <!-- <v-btn icon> -->
    <v-btn color="#2c3e50" class="text-light">
      검색
    </v-btn>
  </v-toolbar>
</template>

<script>
  export default {
    data () {
      return {
        loading: false,
        items: [],
        search: null,
        select: null,
        states: [
         'Spring Season',
         'Independent Activist',
         'Timeleap'
        ],
      }
    },
    watch: {
      search (val) {
        val && val !== this.select && this.querySelections(val)
      },
    },
    methods: {
      querySelections (v) {
        this.loading = true
        // Simulated ajax query
        setTimeout(() => {
          this.items = this.states.filter(e => {
            return (e || '').toLowerCase().indexOf((v || '').toLowerCase()) > -1
          })
          this.loading = false
        }, 500)
      },
    },
  }
</script>

<style lang="scss" scoped>
  .search-box {
    // width: 50%;
    border-radius: 20px;
  }
</style>