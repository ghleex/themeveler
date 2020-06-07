<template>
  <div id="service-create">
    <div class="service-center-title"><i class="far fa-sticky-note mr-3"></i>고객문의 작성</div>
    <div class="service-body">
      <div class="reset">
        <v-btn color="error" outlined class="btn-create text-light" @click="reset"><i class="fas fa-redo-alt mr-1"></i>다시 작성</v-btn>
      </div>
      <v-form ref="form" class="service-create-form" v-model="valid" lazy-validation>
        <v-select color="#607D8B" v-model="select" :items="categorys" item-value="id" item-text="category"
         :rules="categoryRules" label="분류" required></v-select>
        <v-text-field color="#607D8B" v-model="title" :counter="30" :rules="titleRules" label="제목" required></v-text-field>
        <v-textarea color="#607D8B" v-model="content" :rules="contentRules" label="내용" class="mt-4" outlined></v-textarea>
        <v-btn color="#607D8B" :disabled="!valid" class="mr-4 btn-create text-light"
          @click="serviceId !== undefined ? update() : write()">{{ serviceId !== undefined ? "수정" : "작성" }}
          <i class="fas fa-check-circle ml-1"></i></v-btn>
        <v-btn color="error" class="btn-create" @click="serviceId !== undefined ? updatecancel() : addcancel()">취소
          <i class="fas fa-times-circle ml-1"></i></v-btn>
      </v-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "service-create",
  data() {
    return {
      serviceId: "",
      userId: "",
      select: null,
      title: "",
      content: "",
      request_user_id: "",
      is_fixed: "",
      valid: false,
      categoryRules: [v => !!v || "분류를 선택해주세요"],
      titleRules: [
        v => !!v || "제목을 작성해주세요",
        v => (v && v.length <= 30) || "제목을 30자 이내로 작성해주세요",
      ],
      contentRules: [v => !!v || "내용을 작성해주세요"],
      categorys: [] // ["테마","장소","기타 서비스"]
    }
  },
  methods: {
    write() {
      if (this.$refs.form.validate()) {
        var serviceCreateForms = {
          "category": this.select,
          "title": this.title,
          "content": this.content,
          "request_user": this.$store.getters.user_id,
          "is_fixed": false,
        }
        const requestHeader = this.$store.getters.requestHeader
        axios.post(`/articles/customer/${this.userId}/`, serviceCreateForms, requestHeader)
          .then(() => {
            this.$router.push({
              path: '/service'
            })
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    update() {
      if (this.$refs.form.validate()) {
        var serviceUpdateForms = {
          "category": this.select,
          "title": this.title,
          "content": this.content,
          "request_user": this.$store.getters.user_id,
          "is_fixed": this.is_fixed
        }
        const requestHeader = this.$store.getters.requestHeader
        axios.put(`/articles/voice/${this.serviceId}/`, serviceUpdateForms, requestHeader)
          .then(() => {
            this.$router.push({
              path: `/service/detail/${this.serviceId}`
            })
          })
          .catch(error => {
            console.log(error)
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
    const requestHeader = this.$store.getters.requestHeader
    axios.get(`/articles/v_category/`, requestHeader)
      .then(response => {
        this.categorys = response.data
      })
      .catch(error => {
        console.log(error.response)
      })
    this.userId = this.$store.getters.user_id
    this.serviceId = this.$route.params.serviceId
    if (this.serviceId !== undefined) {
      axios.get(`/articles/voice/${this.serviceId}/`, requestHeader)
        .then(response => {
          if (response.data.request_user === this.$store.getters.user_id) {
            this.select = response.data.category
            this.title = response.data.title
            this.content = response.data.content
            this.request_user_id = response.data.request_user
            this.is_fixed = response.data.is_fixed
          } else {
            alert("수정 권한이 없습니다.")
            this.$router.push({
              path: '/service'
            })
          }
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped>
  #service-create {
    margin: 64px auto 0 auto;
    padding: 32px 0 48px 0;
    width: 100%;
    height: 100%;
    background-color: rgb(238, 240, 247);
  }

  #service-create .service-center-title {
    font-family: 'Cafe24Simplehae';
    font-size: 40px;
    margin: 0 auto 0 auto;
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
    margin: 0 auto 0 auto;
    border-radius: 0 0 7px 7px;
    box-shadow: 1px 2px 2px 1px rgb(100, 105, 109);
  }

  .reset {
    text-align: right;
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
