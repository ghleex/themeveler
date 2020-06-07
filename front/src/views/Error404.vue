<template>
  <v-container>
    <v-alert type="error" :value="true" style="margin-top: 80px;">
      <p>404 not found</p>
      <p>페이지를 찾을 수 없습니다.</p>
    </v-alert>
  </v-container>
</template>

<script>
  export default {
    methods: {
      a() {
        document.querySelector("#footer").style.display = 'none'
      }
    },
    mounted() {
      this.a()
    }
  }
</script>

<style scoped>

</style>
