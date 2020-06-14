<template>
  <div class="travel-detail-stepper">
    <div style="margin: 2rem 0 3rem 0;">
      <h1 class="text-light d-inline-block p-2" style="background-color: #2c3e50;">#.{{ themeId }}
        {{ themeArr[themeId-1].name }}</h1>
      <h2 class="my-10">{{ e1 }} / {{ dests.length }}</h2>
    </div>
  

    <!-- 길 찾기 -->
    <div class="find-road-btn text-end">
      <v-btn dark color="#2c3e50" rounded @click.stop="navigationUrl(1)">
        <i class="fas fa-map-marker-alt mr-1 text-danger"></i>
        길 찾기
      </v-btn>
    </div>
    <v-dialog v-model="dialog" fullscreen transition="dialog-bottom-transition">
      <v-card>
        <v-card-actions>
          <v-btn class="mx-auto" rounded color="#90A4AE" text @click="dialog = false" style="font-size: 30px; height: 60px !important; background: #ECEFF1">
            <i class="fas fa-times"></i>
          </v-btn>
        </v-card-actions>
        <v-card-text>
          <div class="mt-3 text-center" style="font-size: 12px;">
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
          <v-btn class="my-3" rounded color="#ECEFF1">🚩 {{ progress }}%</v-btn>
          </div>
        </v-card-text>
        <object
          id="naviMap"
          type="text/html"
          :data="mapUrl"
          >
        </object>
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
          </template>
        </v-stepper-header>
      </v-slide-group>

      
      <!-- stepper content -->
      <v-stepper-items>
        <v-img :src="`${baseURL}/${dests[e1-1].image}`"></v-img>
        <v-stepper-content height="auto" v-for="n in steps" :key="`${n}-content`" :step="n">
          <div class="travel-start-text holder mt-5" data-aos="fade-up" data-aos-duration="3000" v-for="i in content"
            :key="i.id">
            <v-card v-if="i.text && i.image" class="holder stepper-text-box" color="rgb(248, 248, 246)">
              <v-img :src="`${baseURL}/${i.image}`"></v-img>
              <b>{{ i.text }}</b>
            </v-card>
            <v-card v-else-if="i.text" class="holder stepper-text-box" color="rgb(248, 248, 246)">
              {{ i.text }}
            </v-card>
            <v-card v-else class="holder stepper-text-box">
              <v-img :src="`${baseURL}/${i.image}`"></v-img>
            </v-card>
          </div>

          <div class="start-next-btn-box" v-if="e1 < dests.length" >
            <v-btn
              dark color="#2c3e50" 
              rounded 
              @click.stop="navigationUrl(0)">
              <i class="fas fa-map-marker-alt mr-1 text-danger"></i>
              다음 장소 {{dests[e1].name}}까지 길 찾기
            </v-btn>

            <v-btn class="start-next-btn" v-if="e1 !== steps" color="red" dark @click="nextStep(n)">
              다음
              <i class="fas fa-chevron-circle-right ml-1"></i>
            </v-btn>
          </div>

          <Complete :themeId=themeId v-else-if="e1 == dests.length" />

          <div v-if="e1 !== 1 && e1 !== dests.length" class="d-flex justify-content-between mb-5">
            <v-btn class="mr-3" v-if="e1 !== 1" @click="beforeStep(n)" rounded color="">
              이전
              <i class="fas fa-chevron-circle-left ml-1"></i>
            </v-btn>
            <v-btn rounded text color="red" @click="returnDetail(themeId)">닫기 <i class="fas fa-times-circle ml-1"></i>
            </v-btn>
          </div>
          <div class="mb-5" v-else-if="e1 == dests.length">
            <v-btn class="mr-3" v-if="e1 !== 1" @click="beforeStep(n)" rounded color="">
              이전
              <i class="fas fa-chevron-circle-left ml-1"></i>
            </v-btn>
          </div>
          <div v-else class="d-flex justify-content-end mb-5">           
            <v-btn roudned text color="blue" class="mr-4" @click="addDestList(dests[n-1].id)">방문장소에 추가 <i class="fas fa-plus-circle ml-1"></i>
            </v-btn>
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
  import Complete from '@/components/TravelComplete.vue'

  export default {
    name: "TravelStart",
    components: {
      Complete
    },
    props: {
      themeId: Number
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
        mapUrl: "",
        mapStatus: 0,
        baseURL: ""
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
          .then(response => {
            this.content = response.data.pages
          })

        document.getElementById(this.dests[n].id).tabIndex = -1;
        document.getElementById(this.dests[n].id).focus();
      },
      beforeStep(n) {
        this.e1 = n - 1
        this.progress = ((this.e1 / this.dests.length) * 100).toFixed(1)

        const requestHeader = this.$store.getters.requestHeader
        axios.get(`/travels/dest_content/${this.themeId}/${this.e1-1}/`, requestHeader)
          .then(response => {
            this.content = response.data.pages
          })

        document.getElementById(this.dests[n - 1].id).tabIndex = -1;
        document.getElementById(this.dests[n - 2].id).focus();
      },
      returnDetail(themeId) {
        this.$router.push(`/travel/${themeId}/`)
      },
      a() {
        document.querySelector("#footer").style.display = "none"
      },
      //`https://map.kakao.com/?sName=${currentAddr}&eName=${destName}`
      success(position) {
        var flag = this.mapStatus
        var destLat = this.dests[this.e1-flag].latitude
        var destLong = this.dests[this.e1-flag].longitude
        var destName = this.dests[this.e1-flag].name
        var currentLat = position.coords.latitude
        var currentLong = position.coords.longitude
        const requestHeader = {
          headers: {
            Authorization: "KakaoAK " + process.env.VUE_APP_KAKAO_REST_API_KEY
          }
        }
        axios.get(`https://dapi.kakao.com/v2/local/geo/coord2address.json?x=${currentLong}&y=${currentLat}`, requestHeader)
          .then(response2 => {
            var currentAddr = response2.data.documents[0].address.address_name
            if (this.isMobile()) {
              axios.get(`https://dapi.kakao.com/v2/local/geo/transcoord.json?x=${destLong}&y=${destLat}&input_coord=WGS84&output_coord=WCONGNAMUL`, requestHeader)
                .then(response => {
                  console.log(response.data)
                  var destX = response.data.documents[0].x
                  var destY = response.data.documents[0].y
                  this.mapUrl = `https://map.kakao.com/?map_type=TYPE_MAP&target=car&rt=%2C%2C${destX}%2C${destY}&rt1=${currentAddr}&rt2=${destName}&rtIds=%2C&rtTypes=%2C`
                })

            } else {
                this.mapUrl = `https://map.kakao.com/?sName=${currentAddr}&eName=${destName}`
            }
            this.dialog = true
          })
        
      },
      navigationUrl(status) {
        this.mapStatus = status
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(this.success)
        } else {
          alert("위치 정보를 사용할 수 없습니다.")
          return false
        }
      },
      addDestList(dest_id) {
        const token = this.$session.get("jwt")
        const requestHeader = {
          headers: {
            Authorization: "JWT " + token
          }
        }
        var form = {
          "user": this.$store.getters.user_id,
          "destination": dest_id
        }
        axios.post('/travels/visited_dests/', form, requestHeader)
          .then(() => {})
      },
      isMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
      }
    },
    mounted() {
      const script = document.createElement('script');
      script.type="text/javascript" 
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${process.env.VUE_APP_KAKAO_API_KEY}&autoload=false`;
      document.head.appendChild(script);
      script.src = `https://developers.kakao.com/sdk/js/kakao.js`
      document.head.appendChild(script);

      const token = this.$session.get("jwt")
      const requestHeader = {
        headers: {
          Authorization: "JWT " + token
        }
      }
      axios.get(`/travels/destinations/${this.themeId}/0/`, requestHeader)
        .then(response => {
          this.dests = response.data.destinations
          console.log(this.dests)
          this.steps = this.dests.length
        })
      axios.get("/travels/all_theme/", requestHeader)
        .then(response => {
          this.themeArr = response.data.all_theme
        })
      axios.get(`/travels/dest_content/${this.themeId}/${this.e1-1}/`, requestHeader)
        .then(response => {
          this.content = response.data.pages
        })
      this.baseURL = process.env.VUE_APP_IP
      this.a()
    }
  }
</script>

<style>
  #navigationModal{
    height: 100vh;
    width: 100vw;
    position: fixed;
    top: 200px;
    left: 0;
    margin: 0;
    border: 0;
    overflow: hidden;
  }

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

  .start-next-btn-box {
    margin: 0 auto;
    align-items: center;
    width: 290px;
    display: flex;
    flex-direction: column;
  }

  #naviMap {
    width: 100%;
    height: 90vh;
    overflow: auto;
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
