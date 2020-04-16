<template>
  <v-container
    class="mt-5"
    fill-height
    style="background-color: white; padding-top: 1.5em;"
  >
    <!-- STORE -->
    <v-layout wrap mt-5 class="mx-3" md12>
      <!--STORE title-->
      <v-flex md12>
        <p class="ma-0 font-weight-light" style="font-size: 1.8em;">
          Store
        </p>
        <v-divider class="mb-5 mt-1"></v-divider>
      </v-flex>
      <!-- storeImg -->
      <v-flex md3 xs12>
        <v-img :aspect-ratio="1 / 1" src="../assets/storeTemp.png"></v-img>
      </v-flex>
      <!-- store info -->
      <v-flex md6 xs12>
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
      <v-flex md3>
        <div id="map" style="width:100% ;height:300px; z-index:0"></div>
      </v-flex>
      <!--menu -->
      <v-flex md12>
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
      <v-flex md12>
        <p class="ma-0 font-weight-light" style="font-size: 1.8em;">
          Reveiw ({{ reviews.length }}건)
        </p>
        <v-divider class="mb-5 mt-1"></v-divider>
      </v-flex>
      <!--review list-->
      <v-flex md6 v-for="(review, index) in reviews" :key="index">
        <v-row>
          <v-card class="reviewCard">
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
                      {{review.user.id}} ({{curYear-review.user.age+1}}세)
                  </span>
                </v-col>
                <v-col class="py-0" style="align-self: center;text-align: end;">
                  <span>
                    <v-icon v-for="(index) in review.total_score" :key="index" color="yellow lighten-1">mdi-star</v-icon>
                    <v-icon v-for="(index) in (5-review.total_score)" :key="index*10" color="grey lighten-2">mdi-star</v-icon>
                  </span>
                </v-col>
                <!-- <v-col class="py-0">
                    <v-btn fab x-small color="blue lighten-2">
                      <v-icon color="white">mdi-pencil-outline</v-icon>
                    </v-btn>
                    <v-btn fab x-small color="red lighten-2">
                      <v-icon color="white">mdi-trash-can</v-icon>
                    </v-btn>
                </v-col> -->
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
                <v-btn color="blue" text x-small class="pl-0">
                  <u>수정</u>
                </v-btn>
                <v-btn color="blue" text x-small class="pl-0">
                  <u>삭제</u>
                </v-btn>
              </span>
            </v-card-text>
          </v-card>
        </v-row>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import http from '../http-common'
import axios from 'axios'

export default {
  data: () => ({
    store: {},
    menus: [],
    reviews: [],
    totalScore: 0,
    isLoading: true,
    curYear: 0,
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
      const requestReview = http.post('api/SearchReviewbyStoreId', form)

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
