<template>
  <div class="account-box">
    <div class="bg-darker">
      <div class="account-div">

        <div class="container" id="container">
          <div class="form-container sign-up-container">
            <form name="signup" class="form" method="post" @submit.prevent="checkSignup()">
              <h1 style="font-size: 30px;">Create Account</h1>
              <span>or use your email for registration</span>
              <input type="email" placeholder="Email" v-model="credentials.email" />
              <v-row justify="content" style="flex: 0 0;">
                <v-dialog v-model="dialog" max-width="500px">
                  <template v-slot:activator="{ on }">
                    <v-btn color="#FF8A65" small dark v-on="on"
                    style="font-weight: 300;">
                    <i class="fas fa-share-square mr-1"></i>
                    이메일 인증</v-btn>
                  </template>
                  <v-card>
                    <v-card-title>
                      <span class="headline" primary-title style="font-weight: 900;">
                        <i class="far fa-paper-plane mr-1"></i>
                        이메일 인증
                      </span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        
                        <input type="text" placeholder="'-'포함 인증번호를 입력하세요" v-model="emailcertcode" class="mr-2 p-2 mb-2" style="width: 207px; border-radius: 50px; border:2px dotted #0097A7" />
                        <v-btn color="#00ACC1" text rounded @click="checkEmail" style="background: #E0F7FA;">
                          <i class="fas fa-envelope-open-text mr-1"></i>
                          인증번호 전송</v-btn>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="checkEmailCert">
                        <i class="fas fa-check-circle mr-1"></i>
                        확인</v-btn>
                      <v-btn color="blue darken-1" text @click="dialog = false">
                        <i class="fas fa-times-circle mr-1"></i>
                        취소</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-row>
              <input type="text" placeholder="Name" v-model="credentials.nickname" />
              <v-btn color="#FF8A65" small dark @click="checkNickname"
              style="font-weight: 300">
              <i class="fas fa-share-square mr-1"></i>
              중복 확인</v-btn>
              <input type="password" name="pw" placeholder="Password" v-model="credentials.pw" />
              <input type="password" name="rpw" placeholder="Confirm Password" v-model="credentials.rpw" />
              <button class="signupbtn">Sign Up</button>
            </form>
          </div>

          <div class="form-container sign-in-container">
            <form name="signin" class="form" method="post" @submit.prevent="checkSignin()">
              <h1>Login</h1>
              <div class="social-container">
                <a :href="baseURL+'/accounts/social/google/'" class="social"><i class="fab fa-google"></i></a>
                <a :href="baseURL+'/accounts/social/kakao/'" class="social"><i class="fab fa-kaggle"></i></a>
              </div>
              <span>or use your account</span>
              <input type="email" placeholder="Email" v-model="credentials.email" />
              <input type="password" placeholder="Password" v-model="credentials.pw" />
              <a @click="forgotPassword">Forgot your password?</a>
              <button class="loginbtn">Login</button>
            </form>
          </div>
          <div class="overlay-container">
            <div class="overlay">
              <div class="overlay-panel overlay-left">
                <h1 style="font-size: 30px;">Welcome Back!</h1>
                <p>개인 정보를 입력 하고 우리와 함께해요!</p>
                <button class="ghost" id="signIn">Login</button>
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
import axios from 'axios'
import Swal from 'sweetalert2'

  export default {
    name: 'Account',
    data() {
      return {
        // emailRules: [
        //   v => !!v || 'E-mail is required',
        //   v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
        // ],
        dialog: false,
        credentials: {
          email: "",
          checkEmailCert: false,
          nickname: "",
          checkNickname: false,
          pw: "",
          rpw: "",
        },
        emailcertcode: "",
        csrf: "",
        baseURL: ""
      }
    },
    methods: {
      // 회원가입 폼 체크
      checkSignup() {
        // 검증 form
        // 이메일 입력하지 않은 경우
        if (!this.credentials.email) {
          Swal.fire({
            title: "Check Email",
            text: "이메일을 입력하세요.",
            type: "warning",
            timer: 3000
          })
        } 
        // 이메일 valid From
        else if (!this.validEmail(this.credentials.email)) {
          Swal.fire({
            title: "Check Email",
            text: "이메일 형식을 확인하세요.",
            type: "warning",
            timer: 3000
          })
        } else if (this.credentials.checkEmailCert == false) {
          Swal.fire({
            title: "Check Email",
            text: "이메일 인증을 하세요.",
            type: "warning",
            timer: 3000
          })
        } else if (this.credentials.nickname == "") {
          Swal.fire({
            title: "Check Name",
            text: "이름을 입력하세요.",
            type: "warning",
            timer: 3000
          })
        } else if (this.credentials.nickname.length >= 7) {
          Swal.fire({
            title: "Check Name",
            text: "이름은 6자 이하로 가능합니다.",
            type: "warning",
            timer: 3000
          })
        } else if (this.credentials.checkNickname == false) {
          Swal.fire({
            title: "Check Name",
            text: "이름 중복확인을 하세요.",
            type: "warning",
            timer: 3000
          })
        }
        // 길이가 너무 짧은 경우 (8자 미만)
        else if (this.credentials.pw.length < 8) {
          Swal.fire({
            title: "Check Password",
            text: "비밀번호는 8자 이상 입력해주세요.",
            type: "warning",
            timer: 3000
          })
        }
        // 비밀번호와 비밀번호확인이 일치하는지 확인
        else if (this.credentials.pw !== this.credentials.rpw) {
          Swal.fire({
            title: "Repeat Password",
            text: "비밀번호가 일치하지 않습니다.",
            type: "warning",
            timer: 3000
          })
        }
        // 검수를 다 거치고 난 후 회원가입
        else {
          const credentials = {
            'username': this.credentials.email,
            'password': this.credentials.pw,
            'nickname': this.credentials.nickname
          }
          // console.log(credentials)
          axios.post('/accounts/signup/', credentials)
            .then(response => {
              if (response.status==200) {
                alert('회원가입이 완료되었습니다.')
                // 회원가입 후 자동로그인
                var loginforms = new FormData()
                loginforms.append('username', this.credentials.email)
                loginforms.append('password', this.credentials.pw)
                this.$emit('login', loginforms)
              }
              else {
                alert('비밀번호가 너무 일상적인 단어입니다.')
              }
            })
            .catch(err => {
              console.log(err)
            })
        }
      },
      // 닉네임 중복체크
      checkNickname() {
        axios.get(`/accounts/nickname/${this.credentials.nickname}/`)
          .then(response => {
            if (response.status==200) {
              alert('사용 가능한 닉네임입니다.')
              this.credentials.checkNickname = true
            }
            else {
              alert('이미 존재하는 닉네임입니다.')
            }
          })
          .catch(err => {
            console.log(err)
            alert('이미 존재하는 닉네임입니다.')
          })
      },
      // 이메일 중복체크
      checkEmail() {
        if (!`${this.credentials.email}`) {
          alert('이메일을 입력해주세요.')
        }
        else {
          axios.get(`/accounts/username/${this.credentials.email}/`)
            .then(response => {
              if (response.status==200) {
                // 인증번호 전송
                axios.post('/accounts/email/send/', {'username': this.credentials.email})
                  .then(
                    alert('인증번호가 전송되었습니다.')
                  )
                  .catch(err => {
                    console.log(err)
                  })
              }
              else {
                alert('이미 존재하는 이메일(ID)입니다.')
              }
            })
            .catch(err => {
              console.log(err)
              alert('이미 존재하는 이메일(ID)입니다.')
            })
        }
      },
      // 이메일 인증
      checkEmailCert() {
        axios.get(`/accounts/email/auth/${this.credentials.email}/${this.emailcertcode}/`)
          .then(response => {
            if (response.status==200) {
              this.dialog=false
              alert('이메일 인증이 완료되었습니다.')
              this.credentials.checkEmailCert = true
            }
            else {
              alert('이메일 인증에 실패하였습니다.')
            }
          })
          .catch(err => {
            console.log(err)
            alert('이메일 인증에 실패하였습니다.')
          })
      },
      // 로그인 폼 체크
      checkSignin() {
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
        // 검수 후 로그인
        else {
          var loginforms = new FormData()
          loginforms.append('username', this.credentials.email)
          loginforms.append('password', this.credentials.pw)
          this.$emit('login', loginforms)
        }
      },
      a() {
        document.querySelector('#footer').style.display = 'none'
      },
      validEmail: function (email) {
        var mailForm = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        return mailForm.test(email)
      },
      forgotPassword() {
        if (this.validEmail(this.credentials.email)) {
          axios.get(`/accounts/password/${this.credentials.email}/`)
            .then(response => {
              console.log(response)
              alert('해당 이메일로 새로운 비밀번호가 전송되었습니다.')
            })
        }
        else {
          alert('올바른 이메일 형식을 입력해주세요.')
        }
      }
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

      this.baseURL = process.env.VUE_APP_IP
    }
  }
</script>

<style lang="scss" scoped>
  .account-box {
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

  .account-div {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    font-family: 'Montserrat', sans-serif;
    height: 100vh;
    margin: 2rem .5rem 0 .5rem;
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

  @media (max-width: 600px) {
    .account-div form {
      padding: 0 10px;
    }
  }
</style>
