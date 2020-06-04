<template>
  <div class="travel-detail-stepper">

    <div style="margin: 2rem 0 3rem 0;">
      <h1 class="text-light d-inline-block p-2" style="background-color: #2c3e50;">#.{{ themeId }}
        {{ themeArr[themeId-1].name }}</h1>
      <h2 class="my-10">{{ e1 }} / {{ dests.length }}</h2>


      <!-- 길 찾기 -->
      <div class="find-road-btn text-end">
        <v-btn dark color="#2c3e50" rounded @click.stop="dialog = true">
          <i class="fas fa-map-marker-alt mr-1 text-danger"></i>
          길 찾기
        </v-btn>
      </div>
    </div>
    <v-dialog v-model="dialog" max-width="290">
      <v-card>
        <v-card-title class="headline">지도</v-card-title>
        <v-card-text>
          hello....sangwon,,,<br>
          This is.. your needs : {{ e1 }}

          <br>
          <v-btn class="mt-8" rounded>🚩 {{ progress }}%</v-btn>
          <div class="mt-3" style="font-size: 12px;">
            <div v-if="progress < 35">
              천천히 걸어볼까요?💦<br>
              헛둘헛둘!
            </div>
            <div v-else-if="35 <= progress && progress < 69">
              벌써 중간지점이에요!👏
            </div>
            <div v-else-if="69 <= progress">
              이제 거의 다 왔어요!<br>
              조금만 더 힘내볼까요?🥰
            </div>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn rounded color="green darken-1" text @click="dialog = false">
            확인<i class="fas fa-check-circle ml-1"></i>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


    <!-- stepper -->
    <v-stepper v-model="e1" class="theme-start-stepper">
      <v-slide-group class="stepper-start-slide" show-arrows>
        <v-stepper-header>
          <template v-for="n in steps">

            <!--  editable -->
            <v-stepper-step :id="dests[n-1].id" :key="`${n}-step`" :complete="e1 > n" :step="n">
              {{ dests[n-1].name }}
              <i class="fas fa-caret-right swal2-success-circular-line-right" v-if="n !== steps"></i>
            </v-stepper-step>

            <!-- <v-divider v-if="n !== steps" :key="n"></v-divider> -->
          </template>
        </v-stepper-header>
      </v-slide-group>

      <v-stepper-items>
        <v-stepper-content height="auto" v-for="n in steps" :key="`${n}-content`" :step="n">

          <div class="travel-start-text holder mt-5" data-aos="fade-up" data-aos-duration="3000" v-for="i in content" :key="i">
            <v-card class="holder stepper-text-box" color="rgb(248, 248, 246)">
              {{ i.text }}
              <!-- {{ n }} {{ i.id }} -->
              <!-- <v-img :src="'@/assets/' + n + '-' + i.id + '.jpg'"></v-img> -->
            </v-card>
            <div class="text-gray mt-3">
              *이미지 자료
            </div>
          </div>


          <v-btn class="start-next-btn" v-if="e1 !== steps" color="red" dark @click="nextStep(n)">
            다음
            <i class="fas fa-chevron-circle-right ml-1"></i>
          </v-btn>

          <Complete :themeId=themeId v-else-if="e1 == dests.length" />

          <div v-if="e1 !== 1 && e1 !== dests.length" class="d-flex justify-content-between mb-5">
            <v-btn class="mr-3" v-if="e1 !== 1" @click="beforeStep(n)" rounded color="">
              이전
              <i class="fas fa-chevron-circle-left ml-1"></i>
            </v-btn>
            <v-btn roudned text color="red" @click="returnDetail(themeId)">닫기 <i class="fas fa-times-circle ml-1"></i>
            </v-btn>
          </div>

          <div class="mb-5" v-else-if="e1 == dests.length">
            <v-btn class="mr-3" v-if="e1 !== 1" @click="beforeStep(n)" rounded color="">
              이전
              <i class="fas fa-chevron-circle-left ml-1"></i>
            </v-btn>
          </div>

          <div v-else class="d-flex justify-content-end mb-5">
            <v-btn roudned text color="red" @click="returnDetail(themeId)">닫기 <i class="fas fa-times-circle ml-1"></i>
            </v-btn>
          </div>

        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>

  </div>
</template>

<script>
  import axios from 'axios'
  import Complete from '../../components/Complete.vue'

  export default {
    name: 'TravelStart',
    components: {
      Complete,
    },
    props: {
      themeId: Number,
    },
    data() {
      return {
        e1: 1,
        dests: [],
        nowDest: "",
        steps: 1,
        themeArr: [],
        content: [],
        dialog: false,
        progress: 0,
      }
    },
    methods: {
      nextStep(n) {
        if (n === this.dests.length) {
          this.e1 = 1
        } else {
          this.e1 = n + 1
          this.progress = ((this.e1 / this.dests.length) * 100).toFixed(1)
        }
        // 다음 detination script 가져오기
        const requestHeader = this.$store.getters.requestHeader
        axios.get(`/travels/dest_content/${this.themeId}/${this.e1-1}/`, requestHeader)
          .then(res => {
            // this.content = res.data
            console.log(res.data)
            this.content = res.data.pages
          })
          .catch(err => {
            console.log(err.response)
          })

        document.getElementById(this.dests[n].id).tabIndex = -1;
        document.getElementById(this.dests[n].id).focus();
      },
      beforeStep(n) {
        this.e1 = n - 1
        // Math.around ?
        this.progress = ((this.e1 / this.dests.length) * 100).toFixed(1)

        const requestHeader = this.$store.getters.requestHeader
        axios.get(`/travels/dest_content/${this.themeId}/${this.e1-1}/`, requestHeader)
          .then(res => {
            // this.content = res.data
            console.log(res.data)
            this.content = res.data.pages
          })
          .catch(err => {
            console.log(err.response)
          })

        document.getElementById(this.dests[n - 1].id).tabIndex = -1;
        document.getElementById(this.dests[n - 2].id).focus();
      },
      returnDetail(themeId) {
        this.$router.push(`/travel/${themeId}/`)
      },
      a() {
        // document.querySelector("#navbar").style.display = 'none'
        document.querySelector("#footer").style.display = 'none'
      }
    },
    mounted() {
      const token = this.$session.get('jwt')
      const requestHeader = {
        headers: {
          Authorization: "JWT " + token
        }
      }

      axios.get(`/travels/destinations/${this.themeId}`, requestHeader)
        .then(res => {
          this.dests = res.data.destinations
          this.steps = this.dests.length
        })
      axios.get("/travels/all_theme/", requestHeader)
        .then(res => {
          this.themeArr = res.data.all_theme
        })

      axios.get(`/travels/dest_content/${this.themeId}/${this.e1-1}/`, requestHeader)
        .then(res => {
          // this.content = res.data
          console.log(res.data)
          this.content = res.data.pages
          // this.te = this.content[0].id
        })
        .catch(err => {
          console.log(err.data)
        })

      this.a()
    }
  }
</script>

<style>
  .find-road-btn {
    margin-right: 10%;
  }

  .travel-start-text {
    margin-bottom: 5rem;
  }

  .start-next-btn {
    border-radius: 100px;
    height: 80px !important;
    margin: 1rem auto 3rem auto;
  }

  .stepper-text-box {
    padding: 1rem;
  }

  .travel-detail-stepper .v-stepper:not(.v-stepper--vertical) .v-stepper__label {
    display: block !important;
    padding-left: .5rem;
    font-size: 20px;
  }

  .travel-detail-stepper {
    padding: 0 10%;
  }

  @media (max-width: 550px) {
    .travel-detail-stepper .v-stepper:not(.v-stepper--vertical) .v-stepper__label {
      font-size: 13px;
    }

    .travel-detail-stepper {
      padding: 0;
    }
  }

  .travel-detail-stepper .v-stepper__step {
    padding: 0 !important;
  }

  .travel-detail-stepper .v-stepper__label>i {
    margin: 0 .7rem;
  }

  .travel-detail-stepper .v-slide-group__content {
    display: flex;
    justify-content: center;
    white-space: nowrap;
  }

  .travel-detail-stepper {
    z-index: 900;
    background-color: #fff;
    height: 100%;
    font-family: 'Cafe24Simplehae';
  }
</style>