<template>
  <v-app id="profile">
    <Drawer class="drawer" />

    <v-content id="profile-content">
      <h2 class="content-title">마이페이지</h2>
      <v-divider></v-divider>
      <v-row justify="center" class="content-body">
        <v-col cols="12" md="6">
          <v-card>
            <h5 class="card-title">
              <span>
                좋아요 누른 장소
                <v-chip class="ma-2 px-2" small color="blue" text-color="white">{{ itemsThemes.length }}</v-chip>
              </span>
            </h5>
            <v-divider></v-divider>
            <v-list>
              <v-list-item v-for="item in itemsThemes" :key="item.name">
                <v-list-item-content>
                  <v-list-item-title>{{ item.name }}</v-list-item-title>
                  <!-- <v-list-item-subtitle>{{ item.subtitle }}</v-list-item-subtitle> -->
                </v-list-item-content>
                <v-list-item-action style="margin-left: auto;">
                  <v-btn icon :to="'/spot/'+item.id"><v-icon color="grey lighten-1">mdi-information</v-icon></v-btn>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card>
            <h5 class="card-title">방문했던 장소
              <span>
                <v-chip class="ma-2 px-2" small color="blue" text-color="white">{{ itemsDests.length }}</v-chip>
                <v-btn class="ma-2" outlined fab x-small color="indigo" @click="updateDest">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
              </span>
            </h5>
            <v-divider></v-divider>
            <v-list>
              <v-list-item v-for="item in itemsDests" :key="item.name + 'asdfasdfsadf'">
                <v-list-item-avatar>
                  <v-checkbox v-model="checked_list" :value="item.id"></v-checkbox>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>{{ item.name }}</v-list-item-title>
                </v-list-item-content>
                <v-list-item-action>
                  <input type="date" v-model="item.visited_at">
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>
      </v-row>
    </v-content>
  </v-app>
</template>

<script>
import axios from 'axios'
import Drawer from '@/components/Drawer.vue'

export default {
  name: "Profile",
  components: {
    Drawer
  },
  data() {
    return {
      itemsThemes: [],
      itemsDests: [],
      checked_list: []
    }
  },
  methods: {
    updateCheck(item) {
      if (this.checked_list.indexOf(item.id) > -1) {
        this.checked_list.splice(this.checked_list.indexOf(item.id), 1)
      } else {
        this.checked_list.push(item.id)
      }
    },
    updateDest() {
      if (this.checked_list.length > 0) {
        if (confirm(`${this.checked_list.length}개의 방문 날짜를 수정합니다.`)) {
          const visited_at = []
          this.itemsDests.forEach(value => {
            if (this.checked_list.indexOf(value.id) > -1) {
              visited_at.push(value.visited_at)
            }
          })
          this.checked_list.sort()
          let data = {
            updated_dests: this.checked_list.join(', '),
            update_dates: visited_at.join(', ')
          }
          console.log(data)
          axios.put('/travels/visited_dests/', data, this.$store.getters.requestHeader)
            .then(() => {
              alert("수정되었습니다.")
            })
            .catch(err => {
              console.log(err)
              alert("수정이 실패하였습니다. 잠시후 다시 시도해주세요.")
            })
        } 
      } else {
        alert('최소 한개의 장소를 선택해야 합니다.')
      }
    }
  },
  mounted() {
    const requestHeader = this.$store.getters.requestHeader
    axios.get('/travels/visited_dests/', requestHeader)
      .then(response => {
        console.log(response)
        this.itemsDests = response.data.visited_dests
      })
      .catch(err => {
        console.log(err)
      })
    
    axios.get('/travels/visited_themes/', requestHeader)
      .then(response => {
        console.log(response)
        this.itemsThemes = response.data.favorite_themes
      })
      .catch(err => {
        console.log(err)
      })
  }
}
</script>

<style scoped>
  #profile {
    margin-top: 64px;
    background-color: rgba(245, 245, 245, 0.5);
  }

  #profile-content {
    margin-left: 256px;
    width: 80%;
  }

  @media (max-width: 600px) {
    #profile-content {
      margin-left: 56px;
      width: 80%;
    }
  }

  .content-title {
    text-align: left;
    margin-left: 20px;
    margin-top: 8px;
  }

  .content-body {
    margin-left: 2px;
    margin-right: 2px;
  }

  .card-title {
    margin-top: 8px;
    margin-bottom: 8px;
    height: 48px;
  }

  .card-title > span {
    line-height: 60px;
  }

  .card-title > span > .v-btn {
    margin-top: 15px !important;
    float: right;
  }
  .v-list {
    height: 30em;
    overflow-y: scroll;
  }

  .v-list::-webkit-scrollbar {
    display:none;
  }
</style>
