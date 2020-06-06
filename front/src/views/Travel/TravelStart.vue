<template>
  <div class="travel-detail-stepper">

    <div style="margin: 2rem 0 3rem 0;">
      <h1 class="text-light d-inline-block p-2" style="background-color: #2c3e50;">#.{{ themeId }}
        {{ themeArr[themeId-1].name }}</h1>
      <h2 class="my-10">{{ e1 }} / {{ dests.length }}</h2>
    </div>



    <!-- 길 찾기 -->
    <div class="find-road-btn text-end">
      <v-btn dark color="#2c3e50" rounded @click.stop="navigationUrl()">
        <i class="fas fa-map-marker-alt mr-1 text-danger"></i>
        길 찾기
      </v-btn>
    </div>
    <v-dialog v-model="dialog" fullscreen transition="dialog-bottom-transition">
      
      <!-- {{ mapUrl }} -->
      
        <v-card>
        <v-card-actions>
            <!-- <v-spacer></v-spacer> -->
             <v-btn class="mx-auto" rounded color="#90A4AE" text @click="dialog = false" style="font-size: 30px; height: 60px !important; background: #ECEFF1">
              <i class="fas fa-times"></i>
            </v-btn>
          </v-card-actions>
          <!-- <v-card-title class="headline">지도</v-card-title> -->
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

        </v-card>
        <iframe id="navigationModal" :src="mapUrl">
      </iframe>
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

          <div class="travel-start-text holder mt-5" data-aos="fade-up" data-aos-duration="3000" v-for="i in content"
            :key="i.text">
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
        mapUrl: "",
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
            // console.log(res.data)
            this.content = res.data.pages
          })
        // .catch(err => {
        //   console.log(err.response)
        // })

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
            // console.log(res.data)
            this.content = res.data.pages
          })
        // .catch(err => {
        //   console.log(err.response)
        // })

        document.getElementById(this.dests[n - 1].id).tabIndex = -1;
        document.getElementById(this.dests[n - 2].id).focus();
      },
      returnDetail(themeId) {
        this.$router.push(`/travel/${themeId}/`)
      },
      a() {
        // document.querySelector("#navbar").style.display = 'none'
        document.querySelector("#footer").style.display = 'none'
      },
      getUrl(result) {
        var start = result[0].address.address_name
        var wayToGo = "car"
        console.log(result)
        // this.mapUrl = `https://map.kakao.com/link/to/${this.dests[this.e1-1].name},${this.dests[this.e1-1].latitude},${this.dests[this.e1-1].longitude}`
        // this.mapUrl = `https://map.kakao.com/?target=${wayToGo}&sName=${start}&eName=${this.dests[this.e1-1].name}`
        this.mapUrl = `https://map.kakao.com/?map_type=TYPE_MAP&target=${wayToGo}&rt=%2C%2C523953%2C1084098&rt1=${start}&rt2=${this.dests[this.e1-1].name}&rtIds=%2C&rtTypes=%2C`
        // window.open(this.mapUrl,"_self")
        this.dialog = true
      },
      getCurrentAddress(arr) {
        var geocoder = new kakao.maps.services.Geocoder();

        function searchDetailAddrFromCoords(lon, lat, callback) {
          geocoder.coord2Address(lon, lat, callback);
        }
        searchDetailAddrFromCoords(arr[1], arr[0], this.getUrl)
      },
      success(position) {
        var arr = new Array()
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        arr.push(latitude)
        arr.push(longitude)
        this.getCurrentAddress(arr)
      },
      navigationUrl() {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(this.success)
        }
      },
    },
    mounted() {
      const script = document.createElement('script')
      script.src = `http://dapi.kakao.com/v2/maps/sdk.js?appkey=${process.env.VUE_APP_KAKAO_API_KEY}&libraries=services`
      document.head.appendChild(script)

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
          // console.log(res.data)
          this.content = res.data.pages
          // this.te = this.content[0].id
        })
      // .catch(err => {
      //   console.log(err.data)
      // })
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
