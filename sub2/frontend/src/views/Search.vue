<template>
  <v-container v-scroll="onScroll" style="background:white">
    <!--auto Complete-->
    <v-layout justify-center wrap mt-5>
      <v-flex md10 xs12>
        <autocomplete
          :search="search"
          placeholder="음식점을 찾아보세요"
          aria-label="Search for a country"
          style="z-index: 10;"
          @submit="onSubmit"
          >
          <template
            #default="{
              rootProps,
              inputProps,
              inputListeners,
              resultListProps,
              resultListListeners,
              results,
              resultProps
            }"
            >
            <div v-bind="rootProps">
              <custom-input
                v-bind="inputProps"
                v-on="inputListeners"
                :class="[
                  'autocomplete-input',
                  { 'autocomplete-input-no-results': noResults },
                  { 'autocomplete-input-focused': focused }
                ]"
                @focus="handleFocus"
                @blur="handleBlur"
                @change="handleChange"
              ></custom-input>
              <ul
                v-if="noResults"
                class="autocomplete-result-list"
                style="position: absolute; z-index: 1; width: 100%; top: 100%;"
              >
                <li class="autocomplete-result">
                  No results found
                </li>
              </ul>
              <v-container
                v-bind="resultListProps"
                v-on="resultListListeners"
                class="pa-0"
                style="background: #ffffff; z-index: 10;  border-color: gray;  border-style: solid; border-radius: 10px;"
              >
                <v-hover
                  v-slot:default="{ hover }"
                  open-delay="50"
                  v-for="(result, index) in results"
                  :key="resultProps[index].id"
                  v-bind="resultProps[index]"
                >
                  <v-card
                    flat
                    :color="
                      hover || findSeleted(resultProps[index])
                        ? '#cccccc'
                        : 'white'
                    "
                    class="px-3"
                    style="z-index: 10;"
                  >
                    <v-row>
                      <v-col class="">
                        <v-icon>mdi-magnify</v-icon>{{ result }}
                      </v-col>
                      <v-col justify-right class="text-right" style="color:gray">
                        상점
                      </v-col>
                    </v-row>
                  </v-card>
                </v-hover>
              </v-container>
            </div>
          </template>
        </autocomplete>
      </v-flex>
    </v-layout>

    <!-- storeList + map -->
    <v-layout wrap mt-5>
      <!-- storeList -->
      <v-flex md9 xs12 v-if="storeSearchList.length != 0">
        <v-layout justify-end md12>
          <v-col class="d-flex py-0" cols="3" sm="3">
          </v-col>
        </v-layout>
        <v-layout wrap>
          <v-flex
            lg4
            md6
            xs12
            v-for="(result,index) in storeSearchList"
            :key="index+'ss'"
            >
            <v-hover v-slot:default="{ hover }">
              <v-card color="grey lighten-4" class="ma-4" :to="'/storeDetail?storeId='+result.id" @mouseenter="doMouseEnterStore(result)">
                <v-img :aspect-ratio="1 / 1" src="../assets/storeTemp.png">
                  <v-expand-transition>
                    <div
                      v-if="hover"
                      class="d-flex transition-fast-in-fast-out cyan lighten-1 v-card--reveal black--text "
                      style="height: 100%; word-break:break-all"
                    >
                      <b
                        v-for="(cate, index) in result.category"
                        :key="index"
                        class="title"
                      >
                        #{{ cate }}
                      </b>
                    </div>
                  </v-expand-transition>
                </v-img>
                <v-card-text class="pt-6" style="position: relative;">
                  <div>
                    <v-rating class="pl-0" v-model="result.total_score" color="yellow lighten-1" hover size="20" background-color="grey lighten-2" dense readonly></v-rating>
                  </div>
                  <div class="title font-weight-light orange--text">
                    {{ result.store_name }}
                  </div>
                  <div
                    class="font-weight-light grey--text caption"
                    style="text-align: left;"
                  >
                    #{{ result.area }}
                    <b
                      v-for="(category, index) in result.category_list"
                      :key="index"
                      class="font-weight-light grey--text caption"
                    >
                      #{{ category }}
                    </b>
                  </div>
                  <div class="font-weight-light body-2 mb-2">
                    {{ result.address }}
                  </div>
                </v-card-text>
              </v-card>
            </v-hover>
          </v-flex>
        </v-layout>
      </v-flex>
      <!-- storeList가 없을 때 -->
      <v-flex md9 xs12 v-if="storeSearchList.length == 0">
        <v-layout justify-end md12>
          <v-col class="d-flex py-0" cols="3" sm="3">
          </v-col>
        </v-layout>
        <v-layout wrap height="400px" class="pt-3">
          <v-sheet
            color="white"
            width="100%"
            style="height: 400px;"
            >
            <v-row
              class="fill-height"
              align="center"
              justify="center"
              >
              <div class="animated shake">
                <p style="text-align-last: center;" >
                  <v-icon style="font-size:100px" color="pink">mdi-account-question</v-icon>
                </p>
                <div class="display-1">검색된 결과가 없습니다.</div>
              </div>
            </v-row>
          </v-sheet>
        </v-layout>
      </v-flex>
      
      <!-- map -->
      <v-flex md3 class="d-none d-md-block">
        <v-col cols=12>
          <div 
            id="map" 
            style="width:100% ;height:400px; z-index:0"
            v-bind:style="{
              top: mapPostion + 'px'
            }"
          ></div>
        </v-col>
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
    <infinite-loading v-if="storeSearchList.length != 0 && loadingState == true" @infinite="infiniteHandler"></infinite-loading>
  </v-container>
</template>

<script>
import Autocomplete from '@trevoreyre/autocomplete-vue'
import { mapMutations, mapState } from 'vuex'
import CustomInput from '@/components/CustomInput'
import http from '../http-common'
import InfiniteLoading from 'vue-infinite-loading';

export default {
  components: {
    Autocomplete,
    CustomInput,
    InfiniteLoading
  },
  data: () => ({
    focused: false,
    value: '',
    results: [],
    keyword: '',
    filterDialog: false,
    orderStandard: 'name',
    storeList: [],
    map: "",
    loading : false,
    sortCondition : ["이름순","별점순","리뷰많은순"],
    loadingState : true,
    mapPostion : 0,
  }),
  created() {
  },
  mounted() {
    window.kakao && window.kakao.maps ? this.initMap() : this.addScript()
  },
  computed: {
    ...mapState("data", ["storeSearchList","storeSearchPage"]),
    noResults() {
      return this.value && this.results.length === 0
    }
  },

  methods: {
    ...mapMutations("data", ["setStoreSearchList","addStoreSearchList","setStoreSearchPage","incrementStoreSearchPage"]),
    handleFocus() {
      this.focused = true
    },

    handleBlur() {
      this.focused = false
    },
    search(input) {
      let form = new FormData()
      form.append('keyword', input)
      this.keyword = input
      // console.log('search')
      return new Promise(resolve => {
        if (input.length < 2) {
          return resolve([])
        }

        http
          .post('/api/SearchStoreforComplete', form)
          .then(response => {
            // console.log(response.data)
            var list = []
            response.data.forEach(element => list.push(element.store_name))
            // console.log(list)
            resolve(list)
          })
          .catch(err => {
            resolve([])
          })
      })
    },
    findSeleted(str) {
      return 'aria-selected' in str
    },
    handleChange(input) {
    },
    onSubmit(result) {
      var keyword
      if (result != undefined && result.length > this.keyword.length) {
        keyword = result
      } else {
        keyword = this.keyword
      }

      this.loadingState = true

      // this.loadingState.reset()
      
      this.setStoreSearchPage(0)
      let form = new FormData()
      form.append('condition', 'storeName')
      form.append('keyword', keyword)
      form.append('count',this.storeSearchPage)
      form.append('size',12)

      // console.log("storeSearchPage : " + this.storeSearchPage)
      
      this.loading = true
      http
        .post('api/searchStore', form)
        .then(response => {
          // console.log(response.data)
          this.loading = false
          if (response.status == 200) {
            // console.log(response.data.storeList)
            this.setStoreSearchList(response.data.storeList)
            this.incrementStoreSearchPage()
          } else {
            this.setStoreSearchList([])
          }

        })
        .catch(err => {
          console.log(err)
        })
    },
    doMouseEnterStore(store) {
      // 마커를 표시할 위치입니다
      var position = new kakao.maps.LatLng(store.latitude, store.longitude)
      // 마커를 생성합니다
      var marker = new kakao.maps.Marker({
        position: position
      })
      // 마커를 지도에 표시합니다.
      marker.setMap(this.map)
      this.map.panTo(position);
      this.map.setLevel(3);
      
      //마커에 커서가 오버됐을 때 마커 위에 표시할 인포윈도우를 생성합니다
      var iwContent = '<div>' + store.store_name + '</div>'
      // 인포윈도우에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
      // 인포윈도우를 생성합니다
      var infowindow = new kakao.maps.InfoWindow({
        content: iwContent
      })
      // 마커에 마우스오버 이벤트를 등록합니다
      kakao.maps.event.addListener(marker, 'mouseover', function() {
        // 마커에 마우스오버 이벤트가 발생하면 인포윈도우를 마커위에 표시합니다
        infowindow.open(this.map, marker)
      })
      // 마커에 마우스아웃 이벤트를 등록합니다
      kakao.maps.event.addListener(marker, 'mouseout', function() {
        // 마커에 마우스아웃 이벤트가 발생하면 인포윈도우를 제거합니다
        infowindow.close()
      })
    },
    initMap() {
      var container = document.getElementById('map')
      var options = {
        center: new kakao.maps.LatLng(36.622423, 127.97399),
        level: 13
      }
      this.map = new kakao.maps.Map(container, options) //마커추가하려면 객체를 아래와 같이 하나 만든다.
      // var marker = new kakao.maps.Marker({ position: map.getCenter() });
      var zoomControl = new kakao.maps.ZoomControl()
      this.map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT)
      // marker.setMap(map);
    },
    addScript() {
      const script = document.createElement('script') /* global kakao */
      script.onload = () => kakao.maps.load(this.initMap)
      script.src =
        'http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=053dd3145f395e73cbb5211bedf3e97f'
      document.head.appendChild(script)
    },
    infiniteHandler($state){
      let form = new FormData()
      form.append('condition', 'storeName')
      form.append('keyword', this.keyword)
      form.append('count',this.storeSearchPage)
      form.append('size',12)

      var tmpList = [];
      http
        .post('api/searchStore', form)
        .then(response => {
          // console.log(response.data.storeList)
          tmpList = response.data.storeList
          if(tmpList.length > 0) {
            this.incrementStoreSearchPage()
            this.addStoreSearchList(tmpList)
            $state.loaded();
          }else{
            this.loadingState = false
            // $state.complete();
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    test(){
      // console.log(this.storeSearchPage)
      this.loading = true
    },
    onScroll(){
      var scroll = window.pageYOffset;
      var fix = 0;
      var move = 0;
      if (scroll > fix) {
        this.mapPostion = move + scroll - fix;
      } else {
        this.mapPostion = move;
      }
    }
  }
}
</script>

<style scoped>
.autocomplete-input-no-results.autocomplete-input-focused {
  border: 3px solid green;
  /* border-bottom-color: transparent;
  border-radius: 8px 8px 0 0; */
}
.autocomplete-input-no-results:not(.autocomplete-input-focused)
  ~ .autocomplete-result-list {
  display: none;
}
input:focus {
  outline: none;
  border: 5px solid green;
}

input {
  border: 5px solid gray;
  border-radius: 20px;
  padding: 20px;
  width: 100%;
}

.v-card {
  margin: 0px;
}

.v-card--reveal {
  align-items: center;
  bottom: 0;
  justify-content: center;
  opacity: 0.7;
  position: absolute;
  width: 100%;
}

.loading-dialog{
  background-color : #303030
}
.list-enter-active, .list-leave-active {
  transition: all 1s;
}
.list-enter, .list-leave-to /* .list-leave-active below version 2.1.8 */ {
  opacity: 0;
  transform: translateY(30px);
}
.list-item {
  display: inline-block;
}
</style>
