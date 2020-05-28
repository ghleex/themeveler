<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <p>token</p>
    <input v-model="token" type="text">
    <br>
    <p>theme</p>
    <input v-model="theme" type="text"><br>
    <button @click="chatHistory">채팅 내용 가져오기</button><br>

    <button @click="handler">방생성</button><br>

    <input @keydown.enter="sendMessage" v-model="message" type="text">
    <button @click="sendMessage">채팅</button>
    <span v-if="memory">
      <p v-for="(text, idx) in memory" :key="idx">{{ text }} {{ text.created_at | moment("YYYY-MM-DD hh:mm:ss") }}</p>
    </span>
    <p v-for="(text, idx) in textarea" :key="idx">{{ text }} {{ text.created_at | moment("YYYY-MM-DD hh:mm:ss") }}</p>
  </div>
</template>

<script>
const axios = require("axios").default;

export default {
  name: "App",
  data:() => {
    return {
      theme: "",
      textarea: [],
      message: "",
      token: "",
      memory: [],
    }
  },

  created() {
    this.$socket.on("message", data => {
      this.textarea.push({
        nickname: data.nickname, 
        message: data.message, 
        theme: this.theme, 
        created_at: this.$moment(new Date()).format("YYYY-MM-DD hh:mm:ss")
      })
    })
  },


  methods: {
    chatHistory() {
      axios.get("http://127.0.0.1:8000/api/travels/chat/" + this.theme + "/", {headers:{Authorization:"jwt " + this.token}})
      .then(res => {
        this.memory = res.data
        this.handler()
      })
      .catch(err => {
        console.log(err)
      })
    },
    checkConnected() {
      return this.$socket.connected
    },
    handler() {
      this.textarea = []
      if (this.checkConnected) {
        this.$socket.emit("startMessage", {theme:this.theme, nickname:this.nickname})
        this.$socket.on("joined", data => {
          data["created_at"] = this.$moment(new Date()).format("YYYY-MM-DD hh:mm:ss")
          this.textarea = [data]
        })
      } else {
        this.textarea = [{theme: "error", nickname: "관리자", message: "에러발생"}]
      }
    },
    sendMessage() {
      var message = this.message
      this.message = ""
      if (this.checkConnected) {
        var data = {"message":message}
        axios.post("http://127.0.0.1:8000/api/travels/chat/" + this.theme + "/", data, {headers:{Authorization:"jwt " + this.token}})
        .then(res =>{
          this.$socket.emit("sendMessage",{theme: this.theme, nickname: res.data.nickname, message: message})
          this.textarea.push(res.data)
        })
        .catch(err =>{
          console.log(err)
          this.textarea = [{theme: "error", nickname: "관리자", message: "에러발생"}]
        })
        
      } else {
        this.textarea = [{theme: "error", nickname: "관리자", message: "에러발생"}]
      }
    },
    
  }

}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
