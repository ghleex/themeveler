<template>
  <v-app id="profiletest">
    <v-card id="lateral">
      <v-toolbar dark tabs flat color="indigo">
        <template>
          <v-tabs v-model="tabs" align-with-title>
            <v-tab href="#one">One</v-tab>
            <v-tab href="#two">Two</v-tab>
            <v-tab href="#three">Three</v-tab>
            <v-tabs-slider color="pink"></v-tabs-slider>
          </v-tabs>
        </template>
      </v-toolbar>
      <v-card-text>
        <v-tabs-items v-model="tabs">
          <v-tab-item v-for="content in ['one', 'two', 'three']" :key="content" :value="content">
            <v-card height="200px" flat></v-card>
          </v-tab-item>
        </v-tabs-items>
      </v-card-text>
      <v-fab-transition>
        <v-btn :key="activeFab.icon" :color="activeFab.color" fab large dark bottom right class="v-btn--example">
          <v-icon>{{ activeFab.icon }}</v-icon>
        </v-btn>
      </v-fab-transition>
    </v-card>
  </v-app>
</template>

<script>
export default {
  data () {
    return {
      fab: false,
      hidden: false,
      tabs: null
    }
  },
  computed: {
    activeFab () {
      switch (this.tabs) {
        case 'one': return { color: 'success', icon: 'share' }
        case 'two': return { color: 'red', icon: 'edit' }
        case 'three': return { color: 'green', icon: 'keyboard_arrow_up' }
        default: return {}
      }
    }
  }
}
</script>

<style>
  #profiletest {
    margin-top: 64px;
  }

  #lateral .v-btn--example {
    bottom: 0;
    position: absolute;
    margin: 0 0 16px 16px;
  }
</style>
