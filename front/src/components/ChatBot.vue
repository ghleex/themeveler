<template>
  <div class="">
    <div class="chatbot-box" @click.stop="dialog = true">
      <i class="fas fa-comment-dots chatbot-icon"></i>
    </div>
    <v-dialog
      v-model="dialog"
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">여행지</v-card-title>

        <v-card-text>
          Hello....Juno Juno,,
        </v-card-text>

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
  export default {
    name: 'ChatBot',
    props: {
      themeId: Number,
    },
    data() {
      return {
        dialog: false,
      }
    },
    methods: {

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