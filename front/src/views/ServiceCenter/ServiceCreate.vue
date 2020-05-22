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
        <v-textarea color="#607D8B" class="mt-4" outlined label="내용" v-model="content" :rules="contentRules"></v-textarea>
        <v-text-field color="#607D8B" class="mb-7" v-model=" writer" label="작성자" required></v-text-field>
        <v-btn color="#607D8B" :disabled="!valid" class="mr-4 text-light btn-create"
          @click="index !== undefined ? update() : write()">{{index !== undefined ? '수정' : '작성'}}
          <i class="fas fa-check-circle ml-1"></i></v-btn>
        <v-btn color="error" class="btn-create" @click="index !== undefined ? updatecancel() : addcancel()">취소
          <i class="fas fa-times-circle ml-1"></i></v-btn>
      </v-form>
    </div>
  </div>
</template>

<script>
  import data from '@/views/ServiceCenter/data'
  import Swal from 'sweetalert2'

  export default {
    name: 'service-create',
    data() {
      const index = this.$route.params.serviceId;
      return {
        data: data,
        index: index,
        select: index !== undefined ? data[index].category : null,
        title: index !== undefined ? data[index].title : "",
        content: index !== undefined ? data[index].content : "",
        writer: index !== undefined ? data[index].writer : "",
        valid: false,
        categoryRules: [[v => !!v || '분류를 선택해주세요']],
        titleRules: [
          v => !!v || '제목을 작성해주세요',
          v => (v && v.length <= 30) || '제목을 30자 이내로 작성해주세요',
        ],
        contentRules: [v => !!v || '내용을 작성해주세요'],
        createddate: "",
        categorys: [
          '건의',
          '신고',
        ]
      }
    },
    methods: {   
      write() {
        var today = new Date();
        var year = today.getFullYear(); // 년도
        var month = today.getMonth() + 1; // 월
        var date = today.getDate(); // 날짜
        // var day = today.getDay(); // 요일
        // var hour = today.getHours() // 시간
        // var min = today.getMinutes()

        // this.createddate = `${year}-${month}-${date} | ${hour}:${min}`
        this.createddate = `${year}-${month}-${date}`
        // console.log(this.createddate)

        this.data.push({
          category: this.select,
          title: this.title,
          content: this.content,
          writer: this.writer,
          createddate: this.createddate
        })

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
          this.$router.push({
            path: '/service'
          })
        }
      },
      update() {
        this.$refs.form.validate()
        data[this.index].category = this.select
        data[this.index].title = this.title
        data[this.index].content = this.content
        data[this.index].writer = this.writer

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
        } else if (!this.content) {
           Swal.fire({
            title: "Check Content",
            text: "내용을 입력하세요.",
            type: "warning",
            timer: 3000
          })
        }

        if (this.$refs.form.validate()) {
          this.$router.push({
            path: '/service'
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
          path: '/service/detail/' + this.index
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
