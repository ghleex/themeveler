<template>
  <div class="travel-detail-stepper">
    <div style="margin: 2rem 0 3rem 0;">
      <h1>#.{{ themeId }} {{ themeArr[themeId-1].name }}</h1>
      <h2 class="my-10">{{ e1 }} / {{ dests.length }}</h2>
    </div>

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
        <v-stepper-content v-for="n in steps" :key="`${n}-content`" :step="n">
          <v-card class="mb-12" color="grey lighten-1" height="200px">
            <div v-for="i in content" :key="i">
              {{ i.text }}
            </div>
          </v-card>

          <v-btn class="mr-3" v-if="e1 !== 1" @click="beforeStep(n)" rounded color="">
            이전
            <i class="fas fa-chevron-circle-left ml-1"></i>
          </v-btn>
          <v-btn rounded v-if="e1 !== steps" color="primary" @click="nextStep(n)">
            다음
            <i class="fas fa-chevron-circle-right ml-1"></i>
          </v-btn>
          <div class="text-end">
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

  export default {
    name: 'TravelStart',
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
      }
    },
    methods: {
      nextStep(n) {
        if (n === this.dests.length) {
          this.e1 = 1
        } else {
          this.e1 = n + 1
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

        document.getElementById(this.dests[n - 1].id).tabIndex;
        document.getElementById(this.dests[n - 2].id).focus();
      },
      returnDetail(themeId) {
        this.$router.push(`/travel/${themeId}/`)
      },
      a() {
        document.querySelector("#Navbar").style.display = 'none'
        document.querySelector("#footer").style.display = 'none'
      }
    },
    mounted() {
      this.a()
      
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
        })
        .catch(err => {
          console.log(err.data)
        })
    }
  }
</script>

<style>
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