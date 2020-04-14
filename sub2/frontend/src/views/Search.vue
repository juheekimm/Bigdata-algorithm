<template>
  <v-container>
    <v-layout justify-center wrap mt-5>
      <v-flex md10 xs12>
        <autocomplete
          :search="search"
          placeholder="음식점을 찾아보세요"
          aria-label="Search for a country"
          @submit="onSubmit"
          style="z-index: 10;"
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
                style="background: #ffffff; z-index: 10;"
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
                        {{ result }}
                      </v-col>
                      <v-col justify-right class="text-right">
                        임시
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
    <v-layout wrap mt-5>
      <v-flex md9 xs12>
        <v-layout justify-end md12>
          <v-btn text @click.stop="filterDialog = true">filter</v-btn>
          <v-dialog v-model="filterDialog" max-width="300">
            <v-card>
              <v-card-title>
                <span class="headline">Filter</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" class="pb-0">
                      정렬순
                      <v-radio-group v-model="orderStandard" column>
                        <v-radio label="이름순" value="name"></v-radio>
                        <v-radio label="리뷰순" value="review"></v-radio>
                        <v-radio label="평점순" value="score"></v-radio>
                      </v-radio-group>
                    </v-col>
                  </v-row>
                  <v-layout justify-end>
                    <v-btn color="primary">적용하기</v-btn>
                  </v-layout>
                </v-container>
              </v-card-text>
            </v-card>
          </v-dialog>
        </v-layout>
        <v-layout wrap>
          <v-flex
            lg4
            md6
            xs12
            v-for="(result, index) in storeList"
            :key="index"
          >
            <v-hover v-slot:default="{ hover }">
              <v-card color="grey lighten-4" class="ma-5" :to="'/storeDetail?storeId='+result.id">
                <v-img :aspect-ratio="1 / 1" src="../assets/storeTemp.png">
                  <v-expand-transition>
                    <div
                      v-if="hover"
                      class="d-flex transition-fast-in-fast-out cyan lighten-1 v-card--reveal black--text "
                      style="height: 100%; word-break:break-all"
                    >
                      <b
                        v-for="(category, index) in result.category_list"
                        :key="index"
                        class="title"
                      >
                        #{{ category }}
                      </b>
                    </div>
                  </v-expand-transition>
                </v-img>
                <v-card-text class="pt-6" style="position: relative;">
                  <v-btn
                    absolute
                    color="pink"
                    class="white--text"
                    fab
                    large
                    right
                    top
                    @click="doMouseEnterStore(result)"
                    style = "z-index:0"
                  >
                    <v-icon>mdi-map-outline</v-icon>
                  </v-btn>
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
      <v-flex md3 class="d-none d-md-block">
        <v-col>
          <div id="map" style="width:100% ;height:400px; z-index:0"></div>
        </v-col>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Card from '@/components/Card'
import StoreListCard from '@/components/StoreListCard'
import Autocomplete from '@trevoreyre/autocomplete-vue'
import { mapState, mapActions } from 'vuex'
import CustomInput from '@/components/CustomInput'
import http from '../http-common'
import axios from 'axios'

export default {
  components: {
    Autocomplete,
    CustomInput
  },
  data: () => ({
    focused: false,
    value: '',
    results: [],
    keyword: '',
    filterDialog: false,
    orderStandard: 'name',
    storeList: []
  }),
  mounted() {
    window.kakao && window.kakao.maps ? this.initMap() : this.addScript()
  },
  computed: {
    noResults() {
      return this.value && this.results.length === 0
    }
  },

  methods: {
    handleFocus() {
      console.log('handleFocus')
      this.focused = true
    },

    handleBlur() {
      console.log('handleBlur')
      this.focused = false
    },
    search(input) {
      let form = new FormData()
      form.append('keyword', input)
      this.keyword = input
      console.log('search')
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
            console.log(list)
            resolve(list)
          })
          .catch(err => {
            resolve([])
          })
      })
    },
    findSeleted(str) {
      console.log('findSeleted')
      return 'aria-selected' in str
    },
    handleChange(input) {
      console.log('handleChange' + ' ' + input.target.value)
    },
    onSubmit(result) {
      var keyword
      if (result != undefined && result.length > this.keyword.length) {
        keyword = result
      } else {
        keyword = this.keyword
      }
      let form = new FormData()
      form.append('condition', 'storeName')
      form.append('keyword', keyword)
      form.append('count', 10)

      http
        .post('api/searchStore', form)
        .then(response => {
          // console.log(response.data)
          if (response.status == 200) {
            console.log(response.data)
            this.storeList = response.data
          } else {
            this.storeList = []
          }
        })
        .catch(err => {
          resolve([])
        })
    },
    doMouseEnterStore(store) {
      console.log('doMouseEnterStore : ' + store)
      var mapContainer = document.getElementById('map'), // 지도를 표시할 div
        mapOption = {
          center: new kakao.maps.LatLng(store.latitude, store.longitude), // 지도의 중심좌표
          level: 3 // 지도의 확대 레벨
        }

      var map = new kakao.maps.Map(mapContainer, mapOption) // 지도를 생성합니다

      // 마커를 표시할 위치입니다
      var position = new kakao.maps.LatLng(store.latitude, store.longitude)
      // 마커를 생성합니다
      var marker = new kakao.maps.Marker({
        position: position
      })
      // 마커를 지도에 표시합니다.
      marker.setMap(map)
      // 마커에 커서가 오버됐을 때 마커 위에 표시할 인포윈도우를 생성합니다

      var iwContent = '<div>' + store.store_name + '</div>'
      // 인포윈도우에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
      // 인포윈도우를 생성합니다
      var infowindow = new kakao.maps.InfoWindow({
        content: iwContent
      })
      // 마커에 마우스오버 이벤트를 등록합니다
      kakao.maps.event.addListener(marker, 'mouseover', function() {
        // 마커에 마우스오버 이벤트가 발생하면 인포윈도우를 마커위에 표시합니다
        infowindow.open(map, marker)
      })
      // 마커에 마우스아웃 이벤트를 등록합니다
      kakao.maps.event.addListener(marker, 'mouseout', function() {
        // 마커에 마우스아웃 이벤트가 발생하면 인포윈도우를 제거합니다
        infowindow.close()
      })
      var zoomControl = new kakao.maps.ZoomControl()
      map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT)
    },
    initMap() {
      var container = document.getElementById('map')
      var options = {
        center: new kakao.maps.LatLng(36.622423, 127.97399),
        level: 13
      }
      var map = new kakao.maps.Map(container, options) //마커추가하려면 객체를 아래와 같이 하나 만든다.
      // var marker = new kakao.maps.Marker({ position: map.getCenter() });
      var zoomControl = new kakao.maps.ZoomControl()
      map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT)
      // marker.setMap(map);
    },
    addScript() {
      const script = document.createElement('script') /* global kakao */
      script.onload = () => kakao.maps.load(this.initMap)
      script.src =
        'http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=053dd3145f395e73cbb5211bedf3e97f'
      document.head.appendChild(script)
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
</style>
