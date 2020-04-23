<template>
  <v-container
    class="mt-5"
    fill-height
    style="background-color: white; padding-top: 1.5em;"
  >
  
    <!-- STORE -->
    <v-layout wrap mt-5 class="mx-3" sm12>
      <!--STORE title-->
      <v-flex sm12 xs12>
        <p class="ma-0 font-weight-light" style="font-size: 1.8em;">
          Store
        </p>
        <v-divider class="mb-5 mt-1"></v-divider>
      </v-flex>
      <!-- storeImg -->
      <v-flex sm3 xs12>
        <v-img :aspect-ratio="1 / 1" src="../assets/storeTemp.png"></v-img>
      </v-flex>
      <!-- store info -->
      <v-flex sm6 xs12>
        <v-row style="align-items: center">
          <v-col>
            <b class="font-weight-bold ml-3" style="font-size: 1.8em;">{{
              store.store_name
            }}</b>
          </v-col>
          <v-col cols="3" sytle="text-align: center;">
            <v-icon color="yellow" style="font-size: 2.5em;">mdi-star</v-icon>
            <b style="font-size: 1.3em; vertical-align: middle;">{{
              totalScore.toFixed(1)
            }}</b>
          </v-col>
        </v-row>
        <v-simple-table class="ma-3">
          <template v-slot:default>
            <tbody>
              <tr>
                <td>지점</td>
                <td>{{ store.branch }}</td>
              </tr>
              <tr>
                <td>지역</td>
                <td>{{ store.area }}</td>
              </tr>
              <tr>
                <td>전화번호</td>
                <td>{{ store.tel }}</td>
              </tr>
              <tr>
                <td>주소</td>
                <td>{{ store.address }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-flex>
      <!-- store map -->
      <v-flex sm3 hidden-xs-only>
        <div id="map" style="width:100% ;height:300px; z-index:0"></div>
      </v-flex>
      <!--menu -->
      <v-flex sm12 xs12>
        <p class="ma-0 font-weight-light" style="font-size: 1.8em;">Menu</p>
        <v-divider class="mb-5 mt-1"></v-divider>

        <div
          v-for="(menu, index) in menus"
          :key="index"
          class="font-weight-light"
        >
          {{ menu.menu_name }} / {{ menu.price.toFixed(0) }}원
        </div>
      </v-flex>

      <!--review title-->
      <v-flex sm12 id ="reviewTitle">
        <p class="ma-0 font-weight-light" style="font-size: 1.8em;">
          Reveiw ({{ reviews.length }}건) 
          <v-btn text @click="reviewDialog = true"><v-icon color="blue">mdi-pencil</v-icon><b>리뷰작성</b></v-btn>
        </p>
        <v-divider class="mb-5 mt-1"></v-divider>
      </v-flex>
      
      <!--review list-->
      <v-flex md6 v-for="(review, index) in reviews" :key="index">
        <v-row>
          <v-hover v-slot:default="{ hover }" open-delay="30">
            <v-card class="reviewCard" :elevation="hover ? 12 : 2">
              <v-list-item-content class="pb-0">
                <v-row>
                  <v-col class="py-0">
                    <span>
                      <v-avatar size="2.2em" color="purple lighten-2" v-if="review.user.gender == '여'">
                        <v-icon color="white">mdi-face-woman</v-icon>
                      </v-avatar>
                      <v-avatar size="2.2em" color="pink lighten-2" v-if="review.user.gender == '남'">
                        <v-icon color="white">mdi-face</v-icon>
                      </v-avatar>
                        {{review.user.nickname == null?"익명":review.user.nickname}} ({{curYear-review.user.age+1}}세)
                    </span>
                  </v-col>
                  <v-col class="py-0" style="align-self: center;text-align: end;">
                    <span>
                      <v-icon v-for="(index) in review.total_score" :key="index" color="yellow lighten-1">mdi-star</v-icon>
                      <v-icon v-for="(index) in (5-review.total_score)" :key="index*10" color="grey lighten-2">mdi-star</v-icon>
                    </span>
                  </v-col>
                </v-row>
              </v-list-item-content>
              <v-card-text class="pa-0 pl-1 pt-1 pb-1">
                <span style="color:#bcbcbc">{{review.reg_time.substring(0,10)}}</span>
              </v-card-text>
              <v-divider></v-divider>
              <v-card-text>
                {{review.content}}
              </v-card-text>
              <v-card-text class="pa-0 pb-3" style="text-align: end;">
                <span>
                  <v-btn color="blue" text x-small class="pl-0" @click="openReviewWindow(review.user.user,review.content,review.total_score,review.id)">
                    <u>수정</u>
                  </v-btn>
                  <v-btn color="blue" text x-small class="pl-0" @click="deleteReview(review.id)">
                    <u>삭제</u>
                  </v-btn>
                </span>
              </v-card-text>
            </v-card>
          </v-hover>
        </v-row>
      </v-flex>
    </v-layout>
    <!-- write review dialog-->
    <v-dialog
        v-model="reviewDialog"
        max-width="500px"
      >
      <!-- 리뷰작성 -->
      <v-card v-if="$cookie.get('token') != null">
        <v-card-title>
          <span class="headline">리뷰작성</span>
        </v-card-title>
        <v-card-text>  
          <v-layout justify-center>
            <div> "<b>{{store.store_name}}</b>"은 어떠셨나요?</div>
          </v-layout>         
        </v-card-text>
        <v-card-text>  
          <v-layout justify-center>
            <v-rating v-model="rating" color="yellow lighten-1" hover size="40" background-color="grey lighten-2" dense></v-rating>
          </v-layout>         
        </v-card-text>
        <v-card-text>  
          <v-layout justify-center>
            <v-textarea
              v-model="contents"
              clearable
              :counter="contentsLength"
              label="리뷰를 작성해주세요"
              outlined
              rows=4
              :rules="[contentRule]"
            ></v-textarea>
          </v-layout>         
        </v-card-text>
        <v-card-actions>
          <v-layout justify-end>
            <v-btn color="primary" text @ @click="reviewDialog = !reviewDialog">Close</v-btn>
            <v-btn color="primary" @click="writeReview">작성</v-btn>
          </v-layout>
        </v-card-actions>
      </v-card>
      
      <!-- 로그인 -->
      <v-card v-if="$cookie.get('token') == null">
        <v-card-title>
          <v-layout justify-center>
            <span class="headline">안내</span>
          </v-layout> 
        </v-card-title>
        <v-card-text class="mt-5">
          <v-layout justify-center>
              <div style="color:red"> 리뷰작성은 로그인 후 가능합니다 </div>
          </v-layout>        
        </v-card-text>
        <v-card-text>
          <v-layout justify-center>
              <loginDialog></loginDialog>
          </v-layout>        
        </v-card-text>
        <v-card-actions>
          <v-layout justify-end>
            <v-btn color="primary" text @click="reviewDialog = !reviewDialog">Close</v-btn>
          </v-layout>
        </v-card-actions>        
      </v-card>
    </v-dialog>
    <!-- update review dialog-->
    <v-dialog
        v-model="reviewUpdateDialog"
        max-width="500px"
      >
      <!-- 리뷰작성 -->
      <v-card>
        <v-card-title>
          <span class="headline">리뷰 수정</span>
        </v-card-title>
        <v-card-text>  
          <v-layout justify-center>
            <div> "<b>{{store.store_name}}</b>"은 어떠셨나요?</div>
          </v-layout>         
        </v-card-text>
        <v-card-text>  
          <v-layout justify-center>
            <v-rating v-model="rating" color="yellow lighten-1" hover size="40" background-color="grey lighten-2" dense></v-rating>
          </v-layout>         
        </v-card-text>
        <v-card-text>  
          <v-layout justify-center>
            <v-textarea
              v-model="contents"
              clearable
              :counter="contentsLength"
              label="리뷰를 작성해주세요"
              outlined
              rows=4
              :rules="[contentRule]"
            ></v-textarea>
          </v-layout>         
        </v-card-text>
        <v-card-actions>
          <v-layout justify-end>
            <v-btn color="primary" text @ @click="reviewUpdateDialog = !reviewUpdateDialog">Close</v-btn>
            <v-btn color="primary" @click="updateReview">수정</v-btn>
          </v-layout>
        </v-card-actions>
      </v-card>
      
    
    </v-dialog>
  </v-container>
</template>

<script>
import http from '../http-common'
import axios from 'axios'
import loginDialog from '../components/loginDialog'

export default {
  components: {
    loginDialog
  },
  data: () => ({
    store: {},
    menus: [],
    reviews: [],
    totalScore: 0,
    isLoading: true,
    curYear: 0,
    reviewDialog : false,
    rating : 4,
    contents : "",
    contentsLength : 300,
    reviewUpdateDialog: false,
    reviewUserId : "",
    reviewId : "",
    
  }),
  created() {
    this.loadData()
    this.calToday()
  },
  mounted() {
    if (!(window.kakao && window.kakao.maps)) this.addScript()
  },
  methods: {
    loadData() {
      this.isLoading = true

      let form = new FormData()
      form.append('storeId', this.$route.query.storeId)

      const requestStore = http.post('/api/SearchStorebyStoreId', form)
      const requestMenu = http.post('/api/SearchMenubyStoreId', form)
      const requestReview = http.post('/api/SearchReviewbyStoreId', form)

      axios
        .all([requestStore, requestMenu, requestReview])
        .then(
          axios.spread((...responses) => {
            const responseStore = responses[0]
            const responseMenu = responses[1]
            const responesReview = responses[2]

            this.store = responseStore.data[0]
            this.menus = responseMenu.data
            this.reviews = responesReview.data

            console.log(this.reviews)

            this.totalScore = 0
            this.reviews.forEach((element) => {
              this.totalScore += element.total_score
            })
            this.totalScore /=
              this.reviews.length == 0 ? 1 : this.reviews.length

            this.isLoading = false

            this.drawMap()
          })
        )
        .catch((errors) => {
          console.log(errors)
        })
    },
    addScript() {
      const script = document.createElement('script') /* global kakao */
      script.onload = () => kakao.maps.load(this.initMap)
      script.src =
        'http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=053dd3145f395e73cbb5211bedf3e97f'
      document.head.appendChild(script)
    },
    drawMap() {
      var container = document.getElementById('map')
      var options = {
        center: new kakao.maps.LatLng(
          this.store.latitude,
          this.store.longitude
        ),
        level: 3,
      }
      var map = new kakao.maps.Map(container, options) //마커추가하려면 객체를 아래와 같이 하나 만든다.
      var marker = new kakao.maps.Marker({ position: map.getCenter() })
      var zoomControl = new kakao.maps.ZoomControl()
      map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT)
      marker.setMap(map)
    },
    calToday() {
      var today = new Date();
      this.curYear = today.getFullYear();
    },
    contentRule() {
      var con = this.contents
      if(con.length > this.contentsLength)
        return this.contentsLength+"자를 넘기지 마세요"
      else
        return true
    },
    writeReview() {
      let form = new FormData()
      form.append('total_score', this.rating)
      form.append('store_id', this.$route.query.storeId)
      form.append('content', this.contents)

      if(this.contentRule() == true){
        var headers = {
          withCredentials: true,
          headers: { 'Authorization': 'jwt '+ this.$cookie.get('token')}
        }
        
      http
        .post('/api/writeReview',form,headers)
        .then(response => {
          console.log(response)
          console.log(response.data)
          this.loadReviewList()
          this.reviewDialog = false

        })
        .catch(err => {
          if(err.response.data.non_field_errors != undefined){
            alert("아이디와 비밀번호를 확인해주세요.")
            this.password = ""
          }else if(err.response.data.password != undefined){
            alert("비밀번호를 확인해주세요.")
            this.password = ""
          }else{
            alert("아이디와 비밀번호를 확인해주세요.")
            this.password = ""
          }
      })
      }else{
        alert("300자이하로 작성해주세요.")
      }
    },
    loadReviewList(){
      let form = new FormData()
      form.append('storeId', this.$route.query.storeId)

      http
        .post('/api/SearchReviewbyStoreId',form)
        .then(response => {
          console.log(response)
          this.reviews = response.data

          this.totalScore = 0
            this.reviews.forEach((element) => {
              this.totalScore += element.total_score
            })
            this.totalScore /=
              this.reviews.length == 0 ? 1 : this.reviews.length

            this.$vuetify.goTo('#reviewTitle', { offset: 0 })
        })
        .catch(err => {
          console.log(err)
        })
    },
    openReviewWindow(userid,content,score,reviewId){
      if(userid == null || this.$cookie.get('token') == null){
        alert("수정 불가 합니다.")
        return;
      }else{
        // 리뷰창 띄우기
        console.log(content)
        this.contents = content
        this.rating = score
        this.reviewUserId = userid
        this.reviewId = reviewId
        this.reviewUpdateDialog = true
      }
    },
    updateReview(userid,content,score){
      let form = new FormData()
      form.append('total_score', this.rating)
      form.append('store_id', this.$route.query.storeId)
      form.append('content', this.contents)
      form.append('userId', this.reviewUserId)
      form.append('reviewId', this.reviewId)

      if(this.contentRule() == true){
        var headers = {
          withCredentials: true,
          headers: { 'Authorization': 'jwt '+ this.$cookie.get('token')}
        }
      
      console.log(this.$cookie.get('token'))
        
      http
        .post('/api/updateReview',form,headers)
        .then(response => {
          var state = response.data.state
          if(state == "success"){
            this.reviewUpdateDialog = false
            this.loadReviewList()

          }else if(state == "fail"){
            alert(response.data.message)
          }
        })
        .catch(err => {
          if(this.$cookie.get('token') == null)
            alert("다시 로그인해주세요")
          else
            alert("서버와 연결이 불안정합니다. 다시 시도해주세요.")
          
      })
      }else{
        alert("300자이하로 작성해주세요.")
      }
    },
    deleteReview(reviewId){
      if(this.$cookie.get('token') == null){
        alert("삭제할 수 없습니다. 로그인 후 시도해보세요.")
        return;
      }else{
        var result = confirm('해당 리뷰를 삭제하겠습니까?');
        if(result == true){ //삭제 요청 
          let form = new FormData()
          form.append('reviewId', reviewId)

          var headers = {
            withCredentials: true,
            headers: { 'Authorization': 'jwt '+ this.$cookie.get('token')}
          }

          http
            .post('/api/deleteReview',form,headers)
            .then(response => {
              var state = response.data.state
              if(state == "success"){
                alert(response.data.message)
                this.loadReviewList()
              }else{
                alert(response.data.message)
              }
            })
            .catch(err => {
              console.log(err)
            })
        }
      }
    },
    test(){
      this.$vuetify.goTo('#reviewTitle', { offset: 0 })
    }
  },
}
</script>

<style scoped>
.reviewCard {
  width: 100%;
  margin-bottom: 1em;
  margin-left:1em;
  margin-right:1em;
  padding-left: 1em;
  padding-right: 1em;
}
</style>
