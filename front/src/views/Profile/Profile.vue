<template>
  <v-app id="profile">
    <Drawer class="drawer" />

    <v-content id="profile-content">
      <h2 class="content-title">마이페이지</h2>
      <v-divider></v-divider>
      <v-row justify="center" class="content-body">
        <v-col cols="12" md="6">
          <v-card>
            <h5 class="card-title">좋아요 누른 장소
              <v-chip class="ma-2 px-2" small color="blue" text-color="white">5</v-chip>
            </h5>
            <v-divider></v-divider>
            <v-list>
              <v-list-item v-for="item in items" :key="item.title" link>
                <v-list-item-avatar>
                  <v-icon :class="[item.iconClass]">{{ item.icon }}</v-icon>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>{{ item.title }}</v-list-item-title>
                  <!-- <v-list-item-subtitle>{{ item.subtitle }}</v-list-item-subtitle> -->
                </v-list-item-content>
                <v-list-item-action>
                  <v-btn icon :to="'/spot/'+item.id"><v-icon color="grey lighten-1">mdi-information</v-icon></v-btn>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card>
            <h5 class="card-title">방문했던 장소
              <v-chip class="ma-2 px-2" small color="blue" text-color="white">5</v-chip>
              <!-- <v-badge color="blue" content="5" inline="true"></v-badge> -->
            </h5>
            <v-divider></v-divider>
            <v-list>
              <v-list-item v-for="item in items" :key="item.title" link>
                <v-list-item-avatar>
                  <v-icon :class="[item.iconClass]">{{ item.icon }}</v-icon>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>{{ item.title }}</v-list-item-title>
                  <v-list-item-subtitle>{{ item.subtitle }}</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <v-btn icon :to="'/spot/'+item.id"><v-icon color="grey lighten-1">mdi-information</v-icon></v-btn>
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
import Drawer from '@/components/Drawer.vue'

export default {
  name: 'Profile',
  components: {
    Drawer
  },
  data() {
    return {
      items: [
        { id: 1, icon: 'mdi-heart-outline', iconClass: 'orange lighten-1 white--text', title: '경복궁', subtitle: 'Jan 9, 2020' },
        { id: 2, icon: 'mdi-heart-outline', iconClass: 'purple lighten-1 white--text', title: '창경궁', subtitle: 'Jan 17, 2020' },
        { id: 3, icon: 'mdi-heart', iconClass: 'red lighten-1 white--text', title: '명동', subtitle: 'Jan 28, 2020' },
        { id: 4, icon: 'mdi-heart', iconClass: 'blue white--text', title: '인사동', subtitle: 'Jan 28, 2020' },
        { id: 5, icon: 'mdi-heart', iconClass: 'amber white--text', title: '청계천', subtitle: 'Jan 28, 2020' },
      ]
    }
  }
}
</script>

<style scoped>
#profile {
  margin-top: 64px;
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
}
</style>
