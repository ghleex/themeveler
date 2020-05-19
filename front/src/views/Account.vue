<template>
  <div class="account-box">
    <div class="bg-darker">
      <div class="account-div">

        <div class="container" id="container">
          <div class="form-container sign-up-container">
            <form name="signup" action="" method="post" @submit.prevent="regiCheck()">
              <h1>Create Account</h1>
              <!-- <div class="social-container">
                <a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
                <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
                <a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
              </div> -->
              <span>or use your email for registration</span>

              <input type="text" placeholder="Name" v-model="credentials.username" />
              <input type="email" placeholder="Email" v-model="credentials.email" />
              <input type="password" name="pw" placeholder="Password" v-model="credentials.pw" />
              <input type="password" name="rpw" placeholder="Confirm Password" v-model="credentials.rpw" />
              <button>Sign Up</button>
            </form>
          </div>
          <div class="form-container sign-in-container">
            <form name="signin" action="" method="post" @submit.prevent="signinCheck()">
              <h1>Sign in</h1>
              <div class="social-container">
                <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
                <a href="#" class="social"><i class="fab fa-kaggle"></i></a>
              </div>
              <span>or use your account</span>
              <input type="email" placeholder="Email" v-model="credentials.email" />
              <input type="password" placeholder="Password" v-model="credentials.pw" />
              <a href="#">Forgot your password?</a>
              <button>Sign In</button>
            </form>
          </div>
          <div class="overlay-container">
            <div class="overlay">
              <div class="overlay-panel overlay-left">
                <h1>Welcome Back!</h1>
                <p>개인 정보를 입력 하고 우리와 함께해요!</p>
                <button class="ghost" id="signIn">Sign In</button>
              </div>
              <div class="overlay-panel overlay-right">
                <h1>Hello, Friend!</h1>
                <p>가입 정보를 기입하고 같이 여행을 떠나요!</p>
                <button class="ghost" id="signUp">Sign Up</button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
  import Swal from 'sweetalert2'

  export default {
    name: 'Account',
    data() {
      return {
        // emailRules: [
        //   v => !!v || 'E-mail is required',
        //   v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
        // ],
        credentials: {
          username: '',
          email: '',
          pw: '',
          rpw: '',
        },
        csrf: '',
      }
    },
    methods: {
      // 로그인 폼 체크
      signinCheck() {
        if (!this.credentials.email) {
          Swal.fire({
            title: "Check Email",
            text: "이메일을 입력하세요.",
            type: "warning",
            timer: 3000
          })
        } else if (!this.credentials.pw) {
          Swal.fire({
            title: "Check Password",
            text: "비밀번호를 입력하세요.",
            type: "warning",
            timer: 3000
          })
        }
        // else {} // 검수 후 로그인
      },

      // 회원가입 폼 체크
      regiCheck() {
        // 검증 form
        // 입력하지 않는 경우 (비어있는 경우)
        if (this.credentials.username == "") {
          Swal.fire({
            title: "Check Name",
            text: "이름을 입력하세요.",
            type: "warning",
            timer: 3000
          })
        } else if (this.credentials.username.length >= 7) {
          Swal.fire({
            title: "Check Name",
            text: "이름은 6자 이하로 가능합니다..",
            type: "warning",
            timer: 3000
          })
        } 
        else if (!this.credentials.email) {
          Swal.fire({
            title: "Check Email",
            text: "이메일을 입력하세요.",
            type: "warning",
            timer: 3000
          })
          // 이메일 valid From
        } 
        else if (!this.validEmail(this.credentials.email)) {
          Swal.fire({
            title: "Check Email",
            text: "이메일 형식을 확인하세요.",
            type: "warning",
            timer: 3000
          })
          }
        // 길이가 너무 짧은 경우 (8자 이하)
        else if (this.credentials.pw.length < 8) {
          Swal.fire({
            title: "Check Password",
            text: "비밀번호는 8자 이상 입력해주세요.",
            type: "warning",
            timer: 3000
          })
        }
        // 비밀번호 확인이 맞는지 확인
        else if (this.credentials.pw !== this.credentials.rpw) {
          Swal.fire({
            title: "Repeat Password",
            text: "비밀번호가 일치하지 않습니다.",
            type: "warning",
            timer: 3000
          })
        }
        // else {} // 검수를 다 거치고 난 후 회원가입
      },
      a() {
        document.querySelector('#footer').style.display = 'none'
      },
      validEmail: function (email) {
        var mailForm =
          /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;        return mailForm.test(email);
      },
    },
    mounted() {
      // footer none
      this.a()

      // signin&up js
      const signUpButton = document.getElementById('signUp');
      const signInButton = document.getElementById('signIn');
      const container = document.getElementById('container');

      signUpButton.addEventListener('click', () => {
        container.classList.add("right-panel-active");
      });

      signInButton.addEventListener('click', () => {
        container.classList.remove("right-panel-active");
      });

      // csrf // :value="scrf"
      // this.$scrfToken;
      // this.csrf = this.$csrf.get();
    }
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

  // account card
  @import url('https://fonts.googleapis.com/css?family=Montserrat:400,800');

  // * {
  //   box-sizing: border-box;
  // }

  .account-div {
    // background: #f6f5f7;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    font-family: 'Montserrat', sans-serif;
    height: 100vh;
    // margin: 0px 0 50px;
  }

  .account-div h1 {
    font-weight: bold;
    margin: 0;
  }

  .account-div p {
    font-size: 14px;
    font-weight: 100;
    line-height: 20px;
    letter-spacing: 0.5px;
    margin: 20px 0 30px;
  }

  .account-div span {
    font-size: 12px;
  }

  .account-div a {
    color: #333;
    font-size: 14px;
    text-decoration: none;
    margin: 15px 0;
  }

  .account-div .social-container>a:hover {
    background-color: rgb(224, 224, 224);
  }

  .account-div .social-container>a:active {
    background-color: rgb(126, 126, 126);
    color: white;
  }

  .account-div button {
    border-radius: 20px;
    border: 1px solid white;
    background-color: rgb(255, 143, 38);
    color: #FFFFFF;
    font-size: 12px;
    font-weight: bold;
    padding: 12px 45px;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: transform 80ms ease-in;
  }

  .account-div button:active {
    transform: scale(0.95);
  }

  .account-div button:focus {
    outline: none;
  }

  .account-div button:hover {
    background-color: rgb(255, 111, 86);
  }

  .account-div button.ghost {
    background-color: transparent;
    border-color: #FFFFFF;
  }

  .account-div form {
    background-color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 0 50px;
    height: 100%;
    text-align: center;
  }

  .account-div input {
    background-color: #eee;
    border: none;
    padding: 12px 15px;
    margin: 8px 0;
    width: 100%;
  }

  .account-div .container {
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25),
      0 10px 10px rgba(0, 0, 0, 0.22);
    position: relative;
    overflow: hidden;
    width: 768px;
    max-width: 100%;
    min-height: 480px;
  }

  .account-div .form-container {
    position: absolute;
    top: 0;
    height: 100%;
    transition: all 0.6s ease-in-out;
  }

  .account-div .sign-in-container {
    left: 0;
    width: 50%;
    z-index: 2;
  }

  .account-div .container.right-panel-active .sign-in-container {
    transform: translateX(100%);
  }

  .account-div .sign-up-container {
    left: 0;
    width: 50%;
    opacity: 0;
    z-index: 1;
  }

  .account-div .container.right-panel-active .sign-up-container {
    transform: translateX(100%);
    opacity: 1;
    z-index: 5;
    animation: show 0.6s;
  }

  @keyframes show {

    0%,
    49.99% {
      opacity: 0;
      z-index: 1;
    }

    50%,
    100% {
      opacity: 1;
      z-index: 5;
    }
  }

  .account-div .overlay-container {
    position: absolute;
    top: 0;
    left: 50%;
    width: 50%;
    height: 100%;
    overflow: hidden;
    transition: transform 0.6s ease-in-out;
    z-index: 10;
  }

  .account-div .container.right-panel-active .overlay-container {
    transform: translateX(-100%);
  }

  .account-div .overlay {
    background: rgb(255, 166, 65);
    background: -webkit-linear-gradient(to right, rgb(255, 125, 38), rgb(255, 189, 90));
    background: linear-gradient(to right, rgb(255, 125, 38), rgb(255, 189, 90));
    // background: #FF416C;
    // background: -webkit-linear-gradient(to right, #FF4B2B, #FF416C);
    // background: linear-gradient(to right, #FF4B2B, #FF416C);
    background-repeat: no-repeat;
    background-size: cover;
    background-position: 0 0;
    color: #FFFFFF;
    position: relative;
    left: -100%;
    height: 100%;
    width: 200%;
    transform: translateX(0);
    transition: transform 0.6s ease-in-out;
  }

  .account-div .container.right-panel-active .overlay {
    transform: translateX(50%);
  }

  .account-div .overlay-panel {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 0 40px;
    text-align: center;
    top: 0;
    height: 100%;
    width: 50%;
    transform: translateX(0);
    transition: transform 0.6s ease-in-out;
  }

  .account-div .overlay-left {
    transform: translateX(-20%);
  }

  .account-div .container.right-panel-active .overlay-left {
    transform: translateX(0);
  }

  .account-div .overlay-right {
    right: 0;
    transform: translateX(0);
  }

  .account-div .container.right-panel-active .overlay-right {
    transform: translateX(20%);
  }

  .account-div .social-container {
    margin: 20px 0;
  }

  .account-div .social-container a {
    border: 1px solid #DDDDDD;
    border-radius: 50%;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    margin: 0 5px;
    height: 40px;
    width: 40px;
  }
</style>