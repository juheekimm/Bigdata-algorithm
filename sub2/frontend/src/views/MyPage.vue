<template>
   <v-container
    class="mt-5"
    style="background-color: white; padding-top: 1.5em; max-width : 800px"
  >
    <!-- STORE -->
    <v-layout wrap mt-5 class="mx-3" >
      <!--STORE title-->
      <v-flex sm12 xs12>
        <p class="ma-0 font-weight-light" style="font-size: 1.8em;">
          MyInfo
        </p>
        <v-divider class="mb-5 mt-1"></v-divider>
      </v-flex>
      <!-- Userimage -->
      <v-flex sm3 hidden-xs-only>
        <v-img :aspect-ratio="1 / 1" src="../assets/woman.png" v-if="user.gender == '여'" class="ma-3"></v-img>
        <v-img :aspect-ratio="1 / 1" src="../assets/man.png" v-if="user.gender == '남'"  class="ma-3"></v-img>
      </v-flex>
      <!-- User Info -->
      <v-flex sm9 xs12>
        <v-simple-table class="ma-3">
          <template v-slot:default>
            <tbody>
              <tr>
                <td colspan="2" class="ma-0 font-weight-bold" style="font-size: 1.3em;" >
                  {{user.nickname}}
                </td>
              </tr>
              <tr>
                <td width="20%">나이</td>
                <td width="80%">{{curYear()-user.age+1}}세</td>
              </tr>
              <tr>
                <td>성별</td>
                <td>{{user.gender == "여" ? "여자" : "남자" }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-flex>
      <!--User Review title-->
      <v-flex sm12 xs12 class="mt-4">
        <p class="ma-0 font-weight-light" style="font-size: 1.8em;">
          Review List
        </p>
        <v-divider class="mb-5 mt-1"></v-divider>
      </v-flex>
      <!--User Review List -->
      <v-flex sm12 v-for="(review, index) in reviews" :key="index" hidden-xs-only>
        <v-hover v-slot:default="{ hover }" open-delay="30">
          <v-card class="reviewCard" :elevation="hover ? 12 : 2" :to="'/storeDetail?storeId='+review.store.id">
            <v-layout wrap row>
              <!-- store info -->
              <v-col cols=12> 
                <div class="d-flex">
                  <v-avatar
                    class="ma-3"
                    size="100"
                    tile
                    > 
                    <v-img :aspect-ratio="1 / 1" src="../assets/storeTemp.png">
                      <v-expand-transition>
                        <div
                          v-if="hover"
                          class="d-flex transition-fast-in-fast-out cyan lighten-1 v-card--reveal black--text "
                          style="height: 100%; word-break:break-all"
                        >
                          <b>상점가기^-^</b>
                        </div>
                      </v-expand-transition>
                    </v-img>
                    
                  </v-avatar>

                  <v-divider vertical inset></v-divider>

                  <div>
                    <v-card-title
                      class="font-weight-bold"
                      v-text="review.store.store_name"
                      name=""
                      style="font-size: 1.3em;"
                    ></v-card-title>
                    <v-rating class="pl-3 pr-5" v-model="review.total_score" color="yellow lighten-1" hover size="35" background-color="grey lighten-2" dense readonly></v-rating>
                    <p class="pl-5 pr-5" v-if="review.store.category != ''">
                      <i
                        v-for="(category, index) in review.store.category.split('|', 2 )"
                        :key="index+'tt'"
                        style="font-size: 0.8em; color: #6e6ee5;"
                      >
                      #{{category}}
                      </i>
                    </p>
                    
                  </div>

                  <v-divider vertical inset></v-divider>

                  <v-card-text class="mx-3 reviewContent" style="">
                    {{review.content}}
                  </v-card-text>                 
                </div>
                  
              </v-col>
              <!-- review Content -->
            </v-layout>
          </v-card>
        </v-hover>
      </v-flex>
      <!-- Mobile User Review List -->
      <v-flex xs12 v-for="(review, index) in reviews" :key="index+'ss'" class="d-flex d-sm-none" wrap>
        <v-hover v-slot:default="{ hover }" open-delay="30">
          <v-card class="mobilereviewCard" :elevation="hover ? 12 : 2" style="width : 100%">
            <v-card-title
              class="font-weight-bold px-1"
              v-text="review.store.store_name"
              name=""
              style="font-size: 1.3em;">
            </v-card-title>
            <v-card-text style="" class="px-1">
              <v-rating v-model="review.total_score" color="yellow lighten-1" hover size="20" background-color="grey lighten-2" dense readonly></v-rating>
            </v-card-text>
            <v-card-text class="mobilereviewContent" style="">
              {{review.content}}
            </v-card-text>     
          </v-card>
        </v-hover>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import http from '../http-common'
import axios from "axios"

export default {
  components: {
  },
  data: () => ({
    user : {},
    reviews : [],
    isLoading : false,
  }),
  created() {
    this.loadData()
    
  },
  mounted() {
    
  },
  methods: {
    loadUserInFo(){
      let form = new FormData()

      var headers = {
          withCredentials: true,
          headers: { 'Authorization': 'jwt '+ this.$cookie.get('token')}
      }
      http
        .post('/api/userbyToken',form,headers)
        .then(response => {
          this.user = response.data[0]
          console.log(this.user)
        })
        .catch(err => {
          console.log(err)
        })
    },
    loadUserReviews(){
      let form = new FormData()

      var headers = {
          withCredentials: true,
          headers: { 'Authorization': 'jwt '+ this.$cookie.get('token')}
      }
      http
        .post('/api/UserReviewbyToken',form,headers)
        .then(response => {
          console.log(response.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
    loadData() {
      // this.isLoading = true

      let form = new FormData()
      var headers = {
          withCredentials: true,
          headers: { 'Authorization': 'jwt '+ this.$cookie.get('token')}
      }

      const requestUser = http.post('/api/userbyToken',form,headers)
      const requestUserReview = http.post('/api/UserReviewbyToken',form,headers)

      axios
        .all([requestUser, requestUserReview])
        .then(
          axios.spread((...responses) => {
            const responseUser = responses[0]
            const responseUserReview = responses[1]

            this.user = responseUser.data[0]
            this.reviews = responseUserReview.data

            console.log(this.user)
            console.log(this.reviews)
          })
        )
        .catch((errors) => {
          console.log(errors)
        })
    },
    curYear() {
      var today = new Date();
      return today.getFullYear();
    },
    test(){

    }
  },
}
</script>

<style scoped>

.v-card--reveal {
  align-items: center;
  bottom: 0;
  justify-content: center;
  opacity: 0.7;
  position: absolute;
  width: 100%;
}

.reviewContent {
  text-align: -webkit-center; 
  border-radius: 10px; 
  background-color: #ededed; 
  border: 4px dashed #bdb5bd;
}

.mobilereviewContent {
  text-align: -webkit-center; 
  border-radius: 10px; 
  background-color: #ededed; 
  border: 2px dashed #bdb5bd;
}

.reviewCard {
  margin-bottom: 1em;
  margin-left:1em;
  margin-right:1em;
  padding-left: 1em;
  padding-right: 1em;
}

.mobilereviewCard {
  margin-bottom: 1em;
  padding-left: 1em;
  padding-right: 1em;
  padding-bottom: 1em;
}

</style>