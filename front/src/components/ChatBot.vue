<template>
  <div class="">
    <div class="chatbot-box" @click="openModal">
      <i class="fas fa-comment-dots chatbot-icon"></i>
    </div>
    <v-dialog
      v-model="dialog"
      max-width="290"
      transition="scale-transition"
    >
      <v-card>
        <v-card-title class="headline">여행지</v-card-title>

        <span v-if="memories">
          <v-card-text v-for="(memory, idx) in memories" :key="idx">
            {{ memory.nickname }} : {{ memory.message }}<br>
            {{ memory.created_at | moment("YYYY-MM-DD hh:mm:ss") }}
          </v-card-text>
        </span>
    
        <span v-if="messages">
          <v-card-text v-for="(message, idx) in messages" :key="idx">
            {{ message.nickname }} : {{ message.message }}<br>
            {{ message.created_at | moment("YYYY-MM-DD hh:mm:ss") }}
          </v-card-text>
        </span>

        <input v-if="connected" type="text" v-model="message" @keypress.enter="sendMessage" style="border: 1px black solid;">
        <span v-else>
          연결안됨
        </span>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="red"
            text
            @click="dialog = false"
          >
            나가기
            <i class="fas fa-times-circle ml-1"></i>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  const axios = require("axios").default;

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
        connected: false
      }
    },
    created() {
      this.$socket.on("message", data => {
        this.messages.push({
          nickname: data.nickname, 
          message: data.message, 
          theme: this.themeId, 
          created_at: this.$moment(new Date()).format("YYYY-MM-DD hh:mm:ss")
        })
      })
    },
    mounted() {
      axios.get(`http://127.0.0.1:8000/api/travels/chat/${this.themeId}/`, this.$store.getters.requestHeader)
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
          data["created_at"] = this.$moment(new Date()).format("YYYY-MM-DD hh:mm:ss")
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
      scroll() {
        var scroll = document.getElementsByClassName('v-dialog')[0]
        scroll.scrollTop = scroll.scrollHeight
      },
      openModal() {
        this.dialog = true
        setTimeout(this.scroll, 10)
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
          axios.post(`http://127.0.0.1:8000/api/travels/chat/${this.themeId}/`, data, this.$store.getters.requestHeader)
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
      },  
    }
    

    
  }
</script>

<style lang="scss" scoped>
  .chatbot-box {
    z-index: 10;
    position: fixed;
    bottom: 100px;
    right: 30px;
    display: flex;
    border-radius: 100px;
    width: 70px;
    height: 70px;
    // background: #994177;
    background: linear-gradient(#ff006a, #ff0c0c);
    justify-content: center;
    align-items: center;
    transition: .2s;
    cursor: pointer;
  }

  .chatbot-box:hover {
    width: 80px;
    height: 80px;
    box-shadow: 2px 2px 3px rgb(104, 110, 110);
  }

  .chatbot-box>i {
    font-size: 35px;
    // color: #2c3e50;
    // color: #ffbc2d;
    color: white;
    // text-shadow: 1px 1px 1px #ffbc2d;;
  }
</style>