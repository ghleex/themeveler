<template>
  <div id="service-create">
    <div class="service-center-title">
      <i class="far fa-sticky-note mr-3"></i>고객문의 작성
    </div>
    <div class="service-body">
      <div class="reset">
        <v-btn color="error" outlined class="btn-create text-light" @click="reset"><i class="fas fa-redo-alt mr-1"></i>다시 작성</v-btn>
      </div>
      <v-form ref="form" class="service-create-form" v-model="valid" lazy-validation>
        <v-select color="#607D8B" v-model="select" :items="categorys" :rules="categoryRules" label="분류" required></v-select>
        <v-text-field color="#607D8B" v-model="title" :counter="30" :rules="titleRules" label="제목" required></v-text-field>
        <v-textarea color="#607D8B" v-model="content" :rules="contentRules" label="내용" class="mt-4" outlined></v-textarea>
        <v-btn color="#607D8B" :disabled="!valid" class="mr-4 text-light btn-create"
          @click="serviceId !== undefined ? update() : write()">{{serviceId !== undefined ? '수정' : '작성'}}
          <i class="fas fa-check-circle ml-1"></i></v-btn>
        <v-btn color="error" class="btn-create" @click="serviceId !== undefined ? updatecancel() : addcancel()">취소
          <i class="fas fa-times-circle ml-1"></i></v-btn>
      </v-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2'

export default {
  name: 'service-create',
  data() {
    return {
      serviceId: "",
      userId: "",
      select: null,
      title: "",
      content: "",
      writer: this.$session.get("nickname"),
      valid: false,
      categoryRules: [v => !!v || '분류를 선택해주세요'],
      titleRules: [
        v => !!v || '제목을 작성해주세요',
        v => (v && v.length <= 30) || '제목을 30자 이내로 작성해주세요',
      ],
      contentRules: [v => !!v || '내용을 작성해주세요'],
      categorys: [
        '건의',
        '신고',
      ]
    }
  },
  methods: {
    write() {
      if (this.select === "건의") {
        this.select = 1
      } else if (this.select === "신고") {
        this.select = 2
      }

      if (this.$refs.form.validate()) {
        var serviceCreateForms = {
          'category': this.select,
          'title': this.title,
          'content': this.content,
          'request_user': this.$store.getters.user_id,
          'is_fixed': "",
        }
        // var today = new Date();
        // var year = today.getFullYear(); // 년도
        // var month = today.getMonth() + 1; // 월
        // var date = today.getDate(); // 날짜
        // // var day = today.getDay(); // 요일
        // // var hour = today.getHours() // 시간
        // // var min = today.getMinutes()

        // // this.writed_at = `${year}-${month}-${date} | ${hour}:${min}`
        // this.writed_at = `${year}-${month}-${date}`
        // // console.log(this.writed_at)

        const requestHeader = this.$store.getters.requestHeader
        axios.post(`/articles/cv/${this.userId}/`, serviceCreateForms, requestHeader)
          .then(
            this.$router.push({
              path: '/service'
            })
          )
          .catch(err => {
            console.log(err)
          })
      }
    },
    update() {
      if (!this.select) {
          Swal.fire({
          title: "Check Categorys",
          text: "분류를 선택해주세요.",
          type: "warning",
          timer: 3000
        })
      } else if (!this.title) {
          Swal.fire({
          title: "Check Title",
          text: "제목을 입력하세요.",
          type: "warning",
          timer: 3000
        })
      } else if (this.title.length > 30) {
          Swal.fire({
          title: "Check Title",
          text: "제목을 30자 이내로 작성해주세요",
          type: "warning",
          timer: 3000
        })
      } else if (!this.content) {
          Swal.fire({
          title: "Check Content",
          text: "내용을 입력하세요.",
          type: "warning",
          timer: 3000
        })
      }

      if (this.$refs.form.validate()) {
        var serviceUpdateForms = {
          'category': this.select,
          'title': this.title,
          'content': this.content,
          'request_user': this.$store.getters.user_id,
          'is_fixed': this.is_fixed
        }
        const requestHeader = this.$store.getters.requestHeader
        axios.put(`/articles/cv/${this.userId}/${this.serviceId}/`, serviceUpdateForms, requestHeader)
          .then(
            this.$router.push({
              path: `/service/detail/${this.serviceId}`
            })
          )
          .catch(err => {
            console.log(err)
          }) 
      }
    },
    reset() {
      this.$refs.form.reset()
    },
    addcancel() {
      this.$router.push({
        path: '/service'
      })
    },
    updatecancel() {
      this.$router.push({
        path: `/service/detail/${this.serviceId}`
      })
    }
  },
  mounted() {
    this.serviceId = this.$route.params.serviceId
    this.userId = this.$store.getters.user_id
    if (this.serviceId !== undefined) {
      axios.get(`/articles/cv/${this.userId}/${this.serviceId}/`)
        .then(response => {
          if (response.data['voice'].request_user === this.$store.getters.user_id) {
            if (response.data.category === 1) {
              this.select = "건의"
            } else if (response.data.category === 2) {
              this.select = "신고"
            }
            this.select = response.data['voice'].category
            this.title = response.data['voice'].title
            this.content = response.data['voice'].content
            this.writer = response.data['voice'].writer_name
            this.is_fixed = response.data['voice'].is_fixed
          } else {
            alert("수정 권한이 없습니다.")
            this.$router.push("/service")
          }
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style scoped>
  #service-create {
    background-color: rgb(238, 240, 247);
    height: 100%;
  }

  .reset {
    text-align: right;
  }

  #service-create .service-center-title {
    font-family: 'Cafe24Simplehae';
    font-size: 40px;
    margin: 8rem auto 0 auto;
    width: 50%;
    border-radius: 7px 7px 0 0;
    box-shadow: 1px 1px 2px 1px rgb(100, 105, 109);
    background-color: rgb(255, 255, 255);
    padding: 2rem 0;
  }

  #service-create .service-body {
    background-color: #fff;
    width: 50%;
    padding: 1.2rem 2rem;
    margin: 0 auto 5rem auto;
    border-radius: 0 0 7px 7px;
    box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
  }

  .btn-create {
    font-family: 'Cafe24Simplehae';
    font-size: 18px;
  }

  .service-create-form {
    padding: 2rem
  }

  @media (max-width: 600px) {
    #service-create .service-body {
      width: 95%;
    }
    #service-create .service-center-title {
      width: 95%;
    }
    .service-create-form {
      padding: 8px;
    }
  }
</style>
