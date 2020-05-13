<template>
  <div class="account-box">
    <div class="bg-darker"></div>
  </div>
</template>

<script>
  export default {
    name: 'Account',
  }
</script>

<style lang="scss" scoped>
  .account-box {
    // margin-top: 64px;
    width: 100vw;
    height: 100vh;
    background-image: url('../assets/image/bg-2.jpg');
    background-repeat: no-repeat;
    background-size: cover;
  }

  .bg-darker {
    background-color: rgba(0, 0, 0, 0.8);
    width: 100%;
    height: 100%;
    position: absolute
  }
</style>