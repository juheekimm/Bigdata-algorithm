<template>
   <v-container class="container">
    <!-- STORE -->
    <v-layout wrap mt-5 class="mx-3" >
      <!--MyInfo title-->
      <v-flex sm12 xs12>
        <p class="ma-0 font-weight-light Do" style="font-size: 1.8em;">
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
      <!--Recommand title-->
      <v-flex sm12 xs12 class="mt-4 outerFlex">
        <span class="ma-0 font-weight-light Do" style="font-size: 1.8em;">
          <v-icon color='red'>mdi-heart</v-icon>여긴 어떠세요?
        </span>
        <span>
          (<b style="color:orange">{{curYear()-user.age+1}}</b>세의 <b style="color:orange">{{user.gender == "여"?"여성":"남성"}}</b>들이 추천합니다.)
        </span>
        <v-divider class="mb-5 mt-1"></v-divider>
        <v-tabs
          background-color="transparent"
          center-active
          height="auto"
          >
          <v-tabs-slider color="transparent"></v-tabs-slider>
          <v-tab v-for="(result,index) in recommandList" :key="index+'ab'" class="pa-0">
            <div>
              <v-hover v-slot:default="{ hover }" >
                <v-card color="grey lighten-4" class="ma-4" :to="'/storeDetail?storeId='+result.id" width="200px">
                  <v-img :aspect-ratio="1 / 1" src="../assets/storeTemp.png">
                    <v-expand-transition>
                      <div
                        v-if="hover"
                        class="d-flex transition-fast-in-fast-out cyan lighten-1 v-card--reveal black--text "
                        style="height: 100%;"
                        >
                        <b
                          v-for="(cate, index) in result.category.split('|')"
                          :key="index"
                          class="title"
                          >
                          #{{ cate }}
                        </b>
                      </div>
                    </v-expand-transition>
                  </v-img>
                  <v-card-text class="pa-1" style="position: relative;">
                    <v-btn
                      absolute
                      :color="getRecommandColor(index)"
                      class="white--text"
                      fab
                      large
                      right
                      top
                    >
                      <v-icon style="font-size:40px">mdi-license</v-icon>
                    </v-btn>
                    <div class="title font-weight-light orange--text">
                      {{ result.store_name }}
                    </div>
                    <div
                      class="font-weight-light grey--text caption"
                      style="text-align: left;"
                      >
                        {{ result.area }}
                    </div>
                  </v-card-text>
                </v-card>
              </v-hover>
            </div>
          </v-tab>
          
        </v-tabs>
      </v-flex>
      <!--User Review title-->
      <v-flex sm12 xs12 class="mt-4">
        <p class="ma-0 font-weight-light Do" style="font-size: 1.8em;">
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
                      class="font-weight-bold pb-0"
                      v-text="review.store.store_name"
                      name="vct"
                      style="font-size: 1.3em;"
                    ></v-card-title>
                    <div
                      name="vas"
                      class="font-weight-light grey--text caption pl-5"
                      v-text="review.store.area"
                    ></div>
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
    <!-- loadingdialog -->
    <v-dialog
      v-model="loading"
      hide-overlay
      persistent
      width="300"
      >
      <v-card
        color="primary"
        dark
        >
        <v-card-text>
          Please stand by
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
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
    loading : false,
    recommandList : [],
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
          // console.log(this.user)
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
          // console.log(response.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
    loadData() {
      this.loading = true

      let form = new FormData()
      var headers = {
          withCredentials: true,
          headers: { 'Authorization': 'jwt '+ this.$cookie.get('token')}
      }

      const requestUser = http.post('/api/userbyToken',form,headers)
      const requestUserReview = http.post('/api/UserReviewbyToken',form,headers)
      const requestReco = http.post('/api/storeRecobytToken',form,headers)
      

      axios
        .all([requestUser, requestUserReview, requestReco ])
        .then(
          axios.spread((...responses) => {
            const responseUser = responses[0]
            const responseUserReview = responses[1]
            const responseReco = responses[2]

            this.user = responseUser.data[0]
            this.reviews = responseUserReview.data
            this.recommandList =responseReco.data
            this.loading = false

            // console.log(responseReco)
            // console.log(this.user)
            // console.log(this.reviews)
          })
        )
        .catch((errors) => {
          console.log(errors)
          alert("마이페이지는 로그인 후 이용가능합니다.")
          his.loading = false
        })
    },
    curYear() {
      var today = new Date();
      return today.getFullYear();
    },
    test(){

    },
    getRecommandColor(index){
      if(index == 0){
        return '#D9D919'
      }else if(index == 1){
        return '#E6E8FA'
      }else if(index == 2){
        return '#A67D3D'
      }else{
        return '#BDBDBD'
      }
    }
  },
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Do+Hyeong&display=swap');
.v-card--reveal {
  align-items: center;
  bottom: 0;
  justify-content: center;
  opacity: 0.7;
  position: absolute;
  width: 100%;
}
.Do {
  font-family: 'Do Hyeon', sans-serif;
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
.container{
  border-style: solid;
  border-color: #82b1ff;
  border-radius: 20px;
  border-width: 8px;
  background-color: white; 
  padding-top: 0.5em; 
  margin-top: 1.5em; 
  max-width : 800px
}

.outerFlex {
  background: #dffbff;
  border-radius: 20px;
  padding: 10px;
  margin-top: 5px;
  margin-bottom: 5px;
}

</style>