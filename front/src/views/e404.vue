<template>
  <v-container>
    <v-alert type="warning" :value="true" style="margin-top: 60px;">
      {{$route.path}} 404 not found
      <p>페이지를 찾을 수 없습니다.</p>
    </v-alert>
  </v-container>
</template>
