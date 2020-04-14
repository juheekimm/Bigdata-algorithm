<template>
  <v-container class="mt-5" fill-height>
    <v-card-text class="text-center">
      <p class="display-2 pa-5">{{ $route.query.storeId }}</p>
      <v-btn @click="test"> 뭐야
      </v-btn>
      <v-btn large color="blue lighten-1 white--text ma-5" rounded to="/search">하이여</v-btn>
    </v-card-text>
  </v-container>
</template>

<script>
export default {
  created(){
      console.log("created하이")
  },
  methods : {
    test() {
      console.log(this.$route.query.storeId)
    }
  }
};
</script>