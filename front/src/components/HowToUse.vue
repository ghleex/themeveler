<template>
  <div>

    <div class="home-how-to-box">
      <div class="home-howTo-img">
        <img :src="info" alt="" class="info-img" width="500px">
      </div>
      <!-- model stepper -->
      <div class="home-howTo-boxBtn">
        <v-btn x-large rounded color="#FF5252" dark @click.stop="dialog = true">
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

                <div class="help-sys-body">
                  <div class="help-sys-img">
                    <v-img src="../assets/image/help1.png" width="80vw" max-width="400px"></v-img>
                  </div>
                  <div class="help-sys-text">
                    #1. 테마블러에서 원하는 테마를 선택하면 <br> 테마에 대한 상세 정보를 알 수 있습니다.
                  </div>
                </div>

                <v-btn rounded color="#EF5350" class="text-light mb-1" @click="e1 = 2">
                  다음
                  <i class="fas fa-arrow-alt-circle-right ml-1"></i>
                </v-btn>
              </v-stepper-content>

              <v-stepper-content step="2">

                <div class="help-sys-body">
                  <div class="help-sys-img">
                    <v-img src="../assets/image/help2.png" height="" width="80vw" max-width="350px"></v-img>
                  </div>
                  <div class="help-sys-text">
                    #2. 테마 상세정보 페이지에서 <br> GO버튼을 찾아 클릭하세요. <br> 즐거운 테마 여행을 안내 받으세요!
                  </div>
                </div>

                <v-btn rounded color="#EF5350" class="text-light mb-1" @click="e1 = 3">
                  다음
                  <i class="fas fa-arrow-alt-circle-right ml-1"></i>
                </v-btn>
              </v-stepper-content>

              <v-stepper-content step="3">

                <div class="help-sys-body">
                  <div class="help-sys-img">
                    <v-img src="../assets/image/help3.png" width="80vw" max-width="400px"></v-img>
                  </div>
                  <div class="help-sys-text">
                    #3. 삽화와 스토리를 통해 <br> 즐거운 시간 보내시길 바랍니다.
                  </div>
                </div>

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
  .home-how-to {
    font-family: 'Cafe24Simplehae';
  }

  .home-how-to-box .v-dialog__content {
    width: 100vw !important;
  }

  .home-how-to-box .v-overlay__scrim {
    width: 100vw;
  }

  .home-how-to-box .v-overlay--active {
    width: 100vw
  }

  .help-sys-body {
    display: flex;
    /* height: 900px; */
    justify-content: center;
    align-items: center;
  }

  @media (max-width: 750px) {
    .help-sys-body {
      flex-direction: column;
    }

    .help-sys-text {
      width: 100% !important;
    }
  }

  .help-sys-img {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .help-sys-text {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem 1rem;
    font-size: 18px;
    font-family: 'Cafe24Simplehae';
    background-color: #2c3e50cb;
    margin-bottom: 1rem;
    border-radius: 5px;
    color: white;
    font-weight: 700;
    width: 50%;
  }
</style>