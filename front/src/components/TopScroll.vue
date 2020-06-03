<template>
  <a id="button" class="hvr-grow" style="display:scroll;">
    <i class="fas fa-arrow-circle-up" style="font-size: 50px;"></i></a>
</template>

<script>
  import JQuery from 'jquery'
  // window.$ = JQuery
  
  // 해당 컴포넌트에서만 jquery를 선언한다는 뜻
  // 한 페이지에만 적용 할 것 이기 때문에
  let $ = JQuery
  export default {
    mounted() {
      var btn = $('#button');
      $(window).scroll(function () {
        if ($(window).scrollTop() > 300) {
          btn.addClass('show');
        } else {
          btn.removeClass('show');
        }
      });
      btn.on('click', function (e) {
        e.preventDefault();
        $('html, body').animate({
          scrollTop: 0
        }, '300');
      });
    }
  }
</script>

<style scoped>
  #button {
    display: inline-block;
    text-align: center;
    position: fixed;
    bottom: 40px;
    right: 25px;
    transition: background-color .3s,
      opacity .5s, visibility .5s;
    opacity: 0;
    visibility: hidden;
    z-index: 1000;
  }

  #button.show {
    opacity: 1;
    visibility: visible;
  }

  #button > i {
    color: #FF5252
  }

  .hvr-grow {
    display: inline-block;
    vertical-align: middle;
    transform: translateZ(0);
    backface-visibility: hidden;
    -moz-osx-font-smoothing: grayscale;
    transition-duration: 0.3s;
    transition-property: transform;
  }
  .hvr-grow:hover,
  .hvr-grow:focus,
  .hvr-grow:active {
    transform: scale(1.1);
  }

  .hvr-grow i:hover {
    text-shadow: 0 0 3px rgb(255, 117, 82);
  }
</style>