<template>
  <div>

    <div class="home-how-to-box">
      <div class="home-howTo-img">
        <img :src="info" alt="" class="info-img" width="500px">
      </div>
      <!-- model stepper -->
      <div class="home-howTo-boxBtn">
        <v-btn x-large rounded color="#FF5252" dark  @click.stop="dialog = true">
          <i class="fas fa-question-circle mr-1"></i>
          How to use Themeveler</v-btn>
      </div>
    </div>




    <v-row justify="center" class="home-how-to">
      <v-dialog v-model="dialog" persistent min-width="350px" width="80vw" max-width="800px">
        <v-card>

          <v-stepper v-model="e1">
            <v-stepper-header>
              <v-stepper-step color="#EF5350" :complete="e1 > 1" step="1">원하는 테마 선택</v-stepper-step>
              <v-divider></v-divider>

              <v-stepper-step color="#EF5350" :complete="e1 > 2" step="2">길 안내에 따른 여행</v-stepper-step>
              <v-divider></v-divider>

              <v-stepper-step color="#EF5350" step="3">맞춤 일러스트 및 스토리 확인</v-stepper-step>
            </v-stepper-header>

            <v-stepper-items>
              <v-stepper-content step="1">
                <v-card class="mb-12" color="grey lighten-1" height="200px"></v-card>
                <v-btn rounded color="#EF5350" class="text-light mb-1" @click="e1 = 2">
                  다음
                  <i class="fas fa-arrow-alt-circle-right ml-1"></i>
                </v-btn>
              </v-stepper-content>

              <v-stepper-content step="2">
                <v-card class="mb-12" color="grey lighten-1" height="200px"></v-card>
                <v-btn rounded color="#EF5350" class="text-light mb-1" @click="e1 = 3">
                  다음
                  <i class="fas fa-arrow-alt-circle-right ml-1"></i>
                </v-btn>
              </v-stepper-content>

              <v-stepper-content step="3">
                <v-card class="mb-12" color="grey lighten-1" height="200px"></v-card>
              </v-stepper-content>
            </v-stepper-items>
          </v-stepper>

          <!-- <v-card-title class="headline">Use Google's location service?</v-card-title>
          <v-card-text>Let Google help apps determine location. This means sending anonymous location data to Google,
            even when no apps are running.</v-card-text> -->

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn v-if="e1 == 3" rounded class="mr-3 mb-3 p-2 stepper-ok-btn" color="#00BCD4" text dark
              @click="clickAgree()">
              알겠어요!
              <i class="fas fa-check-circle ml-1"></i>
            </v-btn>
          </v-card-actions>
        </v-card>

      </v-dialog>
    </v-row>

  </div>
</template>

<script>
  export default {
    name: 'HowToUse',
    data() {
      return {
        e1: 1,
        dialog: false,
        info: require('../assets/info.png'),
      }
    },
    methods: {
      clickAgree() {
        this.e1 = 1
        this.dialog = false
      }
    }
  }
</script>

<style>
 .v-dialog__content {
   width: 100vw !important;
 }

 .v-overlay__scrim {
   width: 100vw;
 }

 .v-overlay--active {
   width: 100vw
 }
</style>