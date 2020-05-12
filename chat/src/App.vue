<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <p>room</p>
    <input v-model="room" type="text">
    <p>username</p>
    <input v-model="userName" type="text">
    <button @click="handler">방생성</button><br>

    <input @keydown.enter="sendMessage" v-model="message" type="text">
    <button @click="sendMessage">채팅</button>
    <p v-for="(text, idx) in textarea" :key="idx">{{ text }}</p>
  </div>
</template>

<script>
export default {
  name: 'App',
  data:() => {
    return {
      room: '',
      userName: '',
      textarea: [],
      message: '',
    }
  },

  created() {
    this.$socket.on('message', data => {
      this.textarea.push({name:data.userName, message:data.message})
    })
  },


  methods: {
    checkConnected() {
      return this.$socket.connected
    },
    handler() {
      if (this.checkConnected) {
        this.textarea = []
        this.$socket.emit('startMessage', {room:this.room, userName:this.userName})
        this.$socket.on('joined', data => {
          this.textarea = [data]
        })
      } else {
        this.textarea = [{room:'error', userName:this.userName, message:'에러발생'}]
      }
    },
    sendMessage() {
      var message = this.message
      this.message = ''
      if (this.checkConnected) {
        this.$socket.emit('sendMessage',{room:this.room, userName:this.userName, message:message})
        this.textarea.push({room:this.room, userName:this.userName, message:message})
      } else {
        this.textarea = [{room:'error', userName:this.userName, message:'에러발생'}]
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
