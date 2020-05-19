<template>
  <v-app id="profile">
    <Drawer class="drawer" />

    <v-content id="profile-content" fluid tag="section">
      <v-row justify="center">
        <v-col cols="12" md="8">


        </v-col>
      </v-row>
    </v-content>
  </v-app>
</template>

<script>
import Drawer from '../components/Drawer.vue'

export default {
  name: 'Profile',
  components: {
    Drawer
  },
  data() {
    return {

    }
  }
}
</script>

<style scoped>
#profile {
  margin-top: 64px;
}

#profile-content {
  margin-left: 256px;
  width: 80%;
}
</style>
