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
import http from '../http-common'
import axios from 'axios';

export default {
  created(){

    this.isLoading = true

    let form = new FormData()
    form.append('storeId',this.$route.query.storeId)

    const requestStore = http.post("/api/SearchStorebyStoreId",form)
    const requestMenu = http.post("/api/SearchMenubyStoreId",form)
    const requestReview = http.post("api/SearchReviewbyStoreId",form)

    axios.all([requestStore, requestMenu, requestReview])
      .then(axios.spread((...responses) => {
        const responseStore = responses[0]
        const responseMenu = responses[1]
        const responesReview = responses[2]

        this.store = responseStore.data[0]
        this.menus = responseMenu.data
        this.reviews = responesReview.data

        this.isLoading = false
   
      }))
      .catch(errors => {

      })
  },
  mounted(){

  },
  methods : {
    test() {
      console.log(this.$route.query.storeId)
    }
  },
  data: () => ({
    store: {},
    menus: [],
    reviews: [],
    isLoading : true,
  }),
};
</script>