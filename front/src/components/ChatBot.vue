<template>
  <div class="chatbot">
    <div class="chatbot-box" @click="openModal">
      <i class="fas fa-comment-dots chatbot-icon"></i>
    </div>
    <v-dialog v-model="dialog" max-width="290" transition="scale-transition">
      <v-card>
        <p v-if="newChat">New Message</p>
        <v-card-title class="headline">여행지</v-card-title>
        <p v-if="chatLoading" class="chatLoading">Loading</p>
        <span v-if="memories">
          <v-card-text v-for="(memory, idx) in memories" :key="idx">
            {{ memory.nickname }} : {{ memory.message }}<br>
            {{ memory.created_at | moment("YYYY-MM-DD LT") }}
          </v-card-text>
        </span>
    
        <span v-if="messages">
          <v-card-text v-for="(message, idx) in messages" :key="idx">
            {{ message.nickname }} : {{ message.message }}<br>
            {{ message.created_at | moment("YYYY-MM-DD LT") }}
          </v-card-text>
        </span>

        <input v-if="connected" type="text" v-model="message" @keypress.enter="sendMessage" style="border: 1px black solid;">
        <span v-else>
          연결안됨
        </span>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red" text @click="dialog = false">
            나가기<i class="fas fa-times-circle ml-1"></i>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  const axios = require("axios").default

  export default {
    name: "ChatBot",
    props: {
      themeId: Number,
    },
    data:() => {
      return {
        theme: "",
        messages: [],
        message: "",
        token: "",
        memories: [],
        dialog: false,
        connected: false,
        chatPage: 1,
        scrollHeight: 0,
        chatLoading: false,
        newChat: false,
        baseURL: ""
      }
    },
    created() {
      this.$socket.on("message", data => {
        let scroll = document.getElementsByClassName("v-dialog")[0]
        let scrollMoveTrigger = Math.round(scroll.scrollTop) == scroll.scrollHeight - scroll.clientHeight
        this.messages.push({
          nickname: data.nickname, 
          message: data.message, 
          theme: this.themeId, 
          created_at: this.$moment(new Date()).format("YYYY-MM-DD LT")
        })
        if (scrollMoveTrigger) {
          this.newChat = false
          setTimeout(() => {
            scroll.scrollTop = scroll.scrollHeight
          }, 40)
        } else {
          this.newChat = true
        }
      })
    },
    mounted() {
      this.baseURL = process.env.VUE_APP_IP

      axios.get(this.baseURL+`/travels/chat/${this.themeId}/${this.chatPage}/`, this.$store.getters.requestHeader)
        .then(res => {
          this.memories = res.data
        })
        .catch(err => {
          console.log(err)
        })
      this.messages = []
      if (this.$socket.connected) {
        this.$socket.emit("startMessage", {theme:this.themeId})
        this.$socket.on("joined", data => {
          data["created_at"] = this.$moment(new Date()).format("YYYY-MM-DD LT")
          this.messages = [data]
          this.connected = true
        })
      } else {
        this.messages = [{theme: "error", nickname: "관리자", message: "에러발생"}]
        this.connected = false
      }
      this.dialog = false
    },
    methods: {
      handleScroll(scrollTop) {
        let scrollMoveTrigger = Math.round(scrollTop.srcElement.scrollTop) == scrollTop.srcElement.scrollHeight - scrollTop.srcElement.clientHeight
        if (scrollTop.srcElement.scrollTop == 0) {
          this.chatLoading = true
          let loadingMessage =  setInterval(() => {
            let loadingText = document.getElementsByClassName("chatLoading")[0]
            loadingText.innerText += "."
            if (loadingText.innerText.length > 10) {
              loadingText.innerText = "Loading"
            }
          }, 100)
          setTimeout(() => {
            this.chatPage += 1
            axios.get(this.baseURL+`/travels/chat/${this.themeId}/${this.chatPage}/`, this.$store.getters.requestHeader)
              .then(res => {
                this.memories = res.data.concat(this.memories)
                setTimeout(() =>{
                  document.getElementsByClassName("v-dialog")[0].scrollTop = this.scrollHeight * res.data.length
                }, 10)
              })
              .catch(err => {
                console.log(err)
                alert("마지막 메시지 입니다.")
              })
            this.chatLoading = false
            clearInterval(loadingMessage)
          }, 1000)
        }
        if (scrollMoveTrigger) {
          this.newChat = false
        }       
      },
      scroll() {
        var scroll = document.getElementsByClassName("v-dialog")[0]
        scroll.scrollTop = scroll.scrollHeight
      },
      openModal() {
        this.dialog = true
        setTimeout(this.scroll, 10)
        setTimeout(() => {
          document.getElementsByClassName("v-dialog")[0].addEventListener("scroll", this.handleScroll)
          this.scrollHeight = document.getElementsByClassName("v-card__text")[0].scrollHeight
        }, 50)
      },
      checkConnected() {
        return this.$socket.connected
      },
      sendMessage() {
        var message = this.message
        this.message = ""
        if (this.checkConnected) {
          let data = {
            "message":message
          }
          axios.post(this.baseURL+`/travels/chat/${this.themeId}/`, data, this.$store.getters.requestHeader)
            .then(res =>{
              this.$socket.emit("sendMessage",{theme: this.themeId, nickname: res.data.nickname, message: message})
              this.messages.push(res.data)
            })
            .catch(err =>{
              console.log(err)
              this.messages = [{theme: "error", nickname: "관리자", message: "에러발생"}]
            })
        } else {
          this.messages = [{theme: "error", nickname: "관리자", message: "에러발생"}]
        }
        setTimeout(this.scroll, 40)
      }
    }
  }
</script>

<style lang="scss" scoped>
  .chatbot-box {
    position: fixed;
    display: flex;
    bottom: 95px;
    right: 25px;
    border-radius: 100px;
    width: 60px;
    height: 60px;
    z-index: 10;
    background: linear-gradient(#ff006a, #ff0c0c);
    justify-content: center;
    align-items: center;
    transition: .2s;
    cursor: pointer;
  }

  .chatbot-box:hover {
    width: 70px;
    height: 70px;
    box-shadow: 2px 2px 3px rgb(104, 110, 110);
  }

  .chatbot-box .fa-comment-dots {
    font-size: 30px;
    // color: #2c3e50;
    // color: #ffbc2d;
    color: white;
    // text-shadow: 1px 1px 1px #ffbc2d;;
  }
</style>
