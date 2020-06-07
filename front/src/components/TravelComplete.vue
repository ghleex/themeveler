<template>
  <div class="complete-box">
    <v-btn class="complete-btn" @click.stop="dialog = true" x-large rounded color="#AD1457" dark>
      수고하셨습니다!🎉
    </v-btn>

    <v-dialog id="complete-dialog" v-model="dialog" width="360">
      <v-card class="complete-card text-center">
        <v-card-title class="headline d-inline-block pt-5">
          <!-- <v-btn color="#E57373" style="font-weight: 400;" large dark> -->
          테마는 어떠셨나요?🥰
          </v-card-title>
        <v-img class="complete-img" :src="img" min-width="300px" max-width="60%"></v-img>
        <v-card-text>
          즐거운 시간이 되었다면 좋겠습니다! <br>
          다음번에도 <b>테마블러와 함께 해주세요!</b>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn rounded color="red" text @click="goDetailPage()">
            알겠어요!
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  export default {
    name: "Complete",
    data() {
      return {
        dialog: false,
        img: require('../assets/complete.png')
      }
    },
    props: {
      themeId: Number,
    },
    methods: {
      goDetailPage() {
        this.$router.push(`/travel/${this.themeId}`, this.themeId)
        this.dialog = false
      }
    }
  }
</script>

<style>
  .complete-btn {
    margin: 3rem auto;
  }

  .complete-box {
    font-family: 'Cafe24Simplehae' !important;
  }

  .complete-img {
    margin: 1rem auto;
  }
</style>