<template>
  <div id="footer" class="container-fluid">
    <!-- <a href="#" target="_blank">
      <i
        @mouseover="githover(1)"
        @mouseleave="githover(0)"
        class="m-4 gitlink fab fa-gitlab"
        size="3x"
        style="color: lightgray"
      ></i>
    </a> -->
    <a class="m-4"></a>
    <div class="row m-0 mx-auto text-white-50 justify-content-around align-items-center" style="max-width: 550px;">
			<p style="color:lightgray;">|</p>
      <p>이길현</p>
      <p style="color:lightgray;">|</p>
      <p>조현호</p>
      <p style="color:lightgray;">|</p>
      <p>박상원</p>
      <p style="color:lightgray;">|</p>
      <p>김준호</p>
      <p style="color:lightgray;">|</p>
      <p>이해인</p>
      <p style="color:lightgray;">|</p>
    </div>

    <div class="row m-0 text-white-50 justify-content-center align-items-center">
      <p> © 2020 Vision2020. All rights reserved.</p>
    </div>

    <div class="row align-items-center m-0">
      <div class="d-none d-md-flex col-md-5">
        <p class="footer-brand">Themeveler</p>
      </div>
      <div class="col offset-md-3">
        <div class="row justify-content-around">
          <router-link to="#" class="footer-right">이용약관</router-link>
          <router-link to="#" class="footer-right">개인정보처리방침</router-link>
          <a href="https://lab.ssafy.com/" target="_blank" class="footer-right"><i class="fab fa-gitlab" /> GitLab</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
    };
  },
  methods: {
  }
};
</script>
<style>
#footer {
  background: #555B6E;
  align-items: center;
  position: relative;
  margin-top: auto !important;
  font-size: calc(6px + 0.6vw)
}
.footer-brand {
  font-size: 2rem;
  font-weight: 900;
  color: lightgray;
  font-family: sans-serif;
  user-select: none;
  margin: 0 !important;
}
.footer-right {
  font-size: calc(6px + 0.5vw);
  color: lightgray !important;
  text-align: left;
  padding: 1rem;
  text-decoration: none !important;
}
.footer-right:hover {
  color: lightgray !important;
}
.gitlink:hover {
  transition: cubic-bezier(0.39, 0.575, 0.565, 1);
  animation: bounce 1s infinite;
  color: lightgray !important;
}
</style>
