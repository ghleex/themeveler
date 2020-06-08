<template>
  <div class="chatbot">
    <div class="chatbot-box" @click="openModal">
      <i class="fas fa-comment-dots chatbot-icon"></i>
    </div>
    <v-dialog content-class="dialog-chat" v-model="dialog" max-width="400" transition="scale-transition">
      <v-card>
        <v-card-title class="headline chatbot-title justify-content-between"
          style="font-family: 'Cafe24Simplehae' !important;">
          <div>
            <i class="fas fa-map-marker-alt mr-2 text-danger"></i>
            {{ themeName }}
          </div>
          <div>
            <v-btn x-large icon @click="dialog = false">
              <i class="far fa-times-circle text-light fa-2x" style="font-style: 50px"></i>
            </v-btn>
          </div>
        </v-card-title>
        
        <div class="chatbot-card">
        <p v-if="chatLoading" class="chatLoading" style="margin-top: 8rem; color: gray;">Loading</p>
        <p style="margin-top: 8rem;"></p>
        <span class="new-message-text">
          <p v-if="newChat" @click="scrollDown" class="text-light bg-danger new-message" style="border-radius: 50px;">New Message</p>
        </span>

        <span v-if="memories">
          <v-card-text class="text-start" v-for="(memory, idx) in memories" :key="idx">
            <span v-if="memory.theme != 'time'">
              <p class="text-start m-0" :class="{'text-dark': anonymous !== memory.nickname}"
                style="font-weight: 500; font-family: 'Cafe24Simplehae' !important;">
                <i class="fas fa-user mr-1"></i>
                {{ memory.nickname }}
              </p>
              <p class="d-inline-block ml-3" :class="{'bg-info': anonymous !== memory.nickname}"
                style="font-family: 'Cafe24Simplehae' !important; max-width: 170px; margin: 0; background: #546E7A; border-radius: 15px; color: white; padding: .5rem .6rem;">
                {{ memory.message }}
              </p>
              <p class="d-inline-block ml-1 text-muted" style="font-weight: 100; font-size: 12px;">
                <i>{{ memory.created_at | checkChatDateTime }}</i>
              </p>
            </span>
            <span v-else>
              <hr>
              <p class="text-center" style="color: gray;">
                <i>{{ memory.message | moment("YYYY-MM-DD") }}</i>
              </p>
            </span>
          </v-card-text>
        </span>

        <span v-if="messages">
          <v-card-text class="text-start" v-for="(message, idx) in messages" :key="idx">
            <span v-if="message.theme != 'time'">
              <p v-if="message.nickname == '공지사항'" class="text-start m-0"
                style="color: #EF5350;font-weight: 700; font-family: 'Cafe24Simplehae' !important;">
                <i class="fas fa-flag mr-1"></i>
                {{ message.nickname }}
              </p>
              <p v-else class="text-start m-0" :class="{'text-info': anonymous !== message.nickname}"
                style="font-family: 'Cafe24Simplehae' !important;">
                <i class="fas fa-user mr-1"></i>
                {{ message.nickname }}
              </p>
              <p v-if="message.nickname !== '공지사항'" :class="{'bg-info': anonymous !== message.nickname}"
                class="d-inline-block ml-3"
                style="max-width: 170px; margin: 0; background: #546E7A; border-radius: 15px; color: white; padding: .5rem .6rem; font-family: 'Cafe24Simplehae' !important;">
                {{ message.message }}
              </p>
              <p v-else class="d-inline-block ml-3"
                style="max-width: 170px; margin: 0; background: #FFF3E0; color: #FF7043; border-radius: 15px; padding: .5rem .6rem; font-family: 'Cafe24Simplehae' !important;">
                {{ message.message }}
              </p>
              <p class="d-inline-block ml-1 text-muted" style="font-weight: 100; font-size: 12px;">
                <i>{{ message.created_at | checkChatDateTime }}</i>
              </p>
            </span>
            <span v-else>
              <hr>
              <p class="text-center" style="color: gray;">
                <i>{{ message.message | moment("YYYY-MM-DD") }}</i>
              </p>
            </span>
          </v-card-text>
        </span>
        </div>
        <v-card-text class="py-5 chat-write" style="background: #ECEFF1;">
          <div v-if="connected">
            <input class="p-1" type="text" v-model="message" @keypress.enter="sendMessage"
              style="border-bottom: 1px #546E7A; background: white; border-radius: 5px;">
            <v-btn @click="sendMessage" class="ml-2" rounded color="#546E7A" small><i class="fas fa-feather"
              style="color: white; padding: 0 !important;"></i></v-btn>
          </div>
          <span class="text-danger" v-else style="font-weight: 700; font-family: 'Cafe24Simplehae' !important;">
            <i class="fas fa-exclamation-triangle mr-1"></i>연결안됨
          </span>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  const axios = require("axios").default
  import Swal from "sweetalert2"

  export default {
    name: "ChatBot",
    computed: {
      anonymous() {
        return this.$store.state.auth.anonymous
      }
    },
    filters: {
      checkChatDateTime(created_at) {
        var now = new Date()
        var date = new Date(created_at)
        var dateDiff = Math.ceil((now.getTime() - date.getTime()) / (60000))
        if (dateDiff <= 1440) {
          var hour = parseInt(dateDiff / 60)
          if (hour) {
            return (`${hour}시간 전`)
          } else {
            var minute = dateDiff % 60
            return (`${minute}분 전`)
          }
        }
        var ap = date.getHours() < 12 ? "AM" : "PM"
        var hourFormat = date.getHours() % 12
        if (hourFormat >= 12) {
          hourFormat %= 12
        }
        return `${hourFormat}:${date.getMinutes()} ${ap}`
      }
    },
    props: {
      themeId: Number,
      themeName: String
    },
    data: () => {
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
        chatDate: [],
        moreData: true
      }
    },
    created() {
      this.$socket.on("message", data => {
        const value = {
          nickname: data.nickname,
          message: data.message,
          theme: this.themeId,
          created_at: this.$moment(new Date()).format("YYYY-MM-DD LT")
        }
        this.addMessage(value)
        let scroll = document.getElementsByClassName("chatbot-card")[0]
        let scrollBottom = scroll.scrollHeight - scroll.clientHeight
        let scrollMoveTrigger = false
        if (scrollBottom - 1 <= Math.round(scroll.scrollTop) && Math.round(scroll.scrollTop) <= scrollBottom + 1) {
          scrollMoveTrigger = true
        }
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
      axios.get(`/travels/chat/${this.themeId}/${this.chatPage}/`, this.$store.getters.requestHeader)
        .then(res => {
          this.addMemories(res.data)
        })
        .catch(err => {
          console.log(err)
        })
      this.messages = []
      this.$socket.emit("startMessage", {
        theme: this.themeId
      })
      this.$socket.on("joined", data => {
        data["created_at"] = this.$moment(new Date()).format("YYYY-MM-DD LT")
        this.messages = [data]
        this.connected = true
      })
      if (this.$socket.connected) {
        this.messages = [{
          theme: "error",
          nickname: "관리자",
          message: "에러발생"
        }]
        this.connected = false
      }
      this.dialog = false
    },
    methods: {
      scrollDown() {
        let scroll = document.getElementsByClassName("chatbot-card")[0]
        scroll.scrollTop = scroll.scrollHeight
      },
      addMessage(value) {
        var created_at = this.$moment(value.created_at).format("YYYY-MM-DD")
        if (this.checkChatDate(created_at)) {
          this.memories.unshift({
            theme: "time",
            nickname: "시간",
            message: value.created_at
          })
        } 
        this.messages.push(value)
      },
      addMemories(values) {
        values.forEach(value => {
          var created_at = this.$moment(value.created_at).format("YYYY-MM-DD")
          if (this.checkChatDate(created_at)) {
            this.memories.unshift({
              theme: "time",
              nickname: "시간",
              message: value.created_at
            })
          } 
          this.memories.splice(1, 0, value)
        })
      },
      checkChatDate(created_at) {
        if (this.chatDate.indexOf(created_at) == -1) {
          this.chatDate.push(created_at)
          return true
        }
        return false
      },
      handleScroll(scrollTop) {
        if (this.moreData == false) {
          return
        }
        let scrollMoveTrigger = Math.round(scrollTop.srcElement.scrollTop) == scrollTop.srcElement.scrollHeight -
          scrollTop.srcElement.clientHeight
        if (scrollTop.srcElement.scrollTop == 0) {
          this.chatLoading = true
          let loadingMessage = setInterval(() => {
            let loadingText = document.getElementsByClassName("chatLoading")[0]
            loadingText.innerText += "."
            if (loadingText.innerText.length > 10) {
              loadingText.innerText = "Loading"
            }
          }, 100)
          setTimeout(() => {
            this.chatPage += 1
            axios.get(`/travels/chat/${this.themeId}/${this.chatPage}/`, this.$store.getters.requestHeader)
              .then(res => {
                this.addMemories(res.data)
                setTimeout(() => {
                  document.getElementsByClassName("chatbot-card")[0].scrollTop = this.scrollHeight * res.data.length
                }, 10)
              })
              .catch(err => {
                console.log(err)
                this.moreData = false
                Swal.fire({
                  title: "Last Message",
                  text: "마지막 메시지 입니다.",
                  icon: "error",
                  timer: 3000
                })
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
        var scroll = document.getElementsByClassName("chatbot-card")[0]
        scroll.scrollTop = scroll.scrollHeight
      },
      openModal() {
        this.dialog = true
        setTimeout(this.scroll, 10)
        setTimeout(() => {
          document.getElementsByClassName("chatbot-card")[0].addEventListener("scroll", this.handleScroll)
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
            "message": message
          }
          axios.post(`/travels/chat/${this.themeId}/`, data, this.$store.getters.requestHeader)
            .then(res => {
              this.$socket.emit("sendMessage", {
                theme: this.themeId,
                nickname: res.data.nickname,
                message: message
              })
              this.addMessage(res.data)
            })
            .catch(err => {
              console.log(err)
              this.messages = [{
                theme: "error",
                nickname: "관리자",
                message: "에러발생"
              }]
            })
        } else {
          this.messages = [{
            theme: "error",
            nickname: "관리자",
            message: "에러발생"
          }]
        }
        setTimeout(this.scroll, 40)
      }
    }
  }
</script>

<style lang="scss">
  .new-message-text {
    position: fixed;
    top: 30%;
  }

  .new-message {
    background-color: rgba(255, 255, 255, 0);
    position: relative;
    right: 48%;
    top: -2rem;
    width: 16rem;
    cursor: pointer;
  }

  .chat-write {
    // position: fixed;
    // bottom: 4rem;
    // width: 310px;
  }

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
    color: white;
  }

  .chatbot-title {
    background-color: #2c3e50;
    color: white;
    top: 6%;
  }

  .chatbot-card {
    overflow-y: scroll;
    height: 23rem;
  }

  .chatbot-card::-webkit-scrollbar {
    width: 5px;
  }

  .chatbot-card::-webkit-scrollbar-thumb {
    background: #2c3e50;
    border-radius: 10px;
  }
</style>