<template>
  <v-container fill-height>
    <v-layout wrap mt-5 class="mx-3" >
      <v-flex sm9>
        <div id="map" style="width:100%;height:100%;"></div>
      </v-flex>
      <v-flex sm3>
        <v-card class="mx-3">
          <v-card-title>
            주변 음식점 찾기
          </v-card-title>
          <v-card-text class="pb-0">
            반경
            <v-divider>
            </v-divider>
            <v-radio-group v-model="distance" row hide-details v-on:change="changeDistance">
              <v-radio label="100m" value="100" selected></v-radio>
              <v-radio label="200m" value="200"></v-radio>
              <v-radio label="300m" value="300"></v-radio>
              <v-radio label="400m" value="400"></v-radio>
            </v-radio-group>
          </v-card-text>
          <v-card-text>
            상점 리스트
            <v-divider>
            </v-divider>
            
            <v-container fill-height class="px-0">
              <v-list
                style="min-height: 400px; max-height: 400px; width:100%"
                class="overflow-y-auto"
              >
                <v-list-item 
                  v-for="(store, index) in storeList"
                  :key="index+'store'"
                  class="pa-0"
                  >
                  <v-hover
                    v-slot:default="{ hover }"
                    open-delay="50"
                    
                  >
                    <v-card
                      flat
                      :color=" hover ? '#B2CCFF' : '#EAEAEA'"
                      class="ma-1 px-3"
                      @mouseenter="enterStoreCard(index)"
                      @mouseleave="leaveStoreCard(index)"
                      :to="'/storeDetail?storeId='+store.id"
                      style="width:100%"
                    >
                      <v-card-text class="subtitle-1 font-weight-bold pa-0 pt-1">
                        {{store.store_name}}
                      </v-card-text>
                      <v-card-text v-for="(cate, index) in store.category.split('|')" :key="index" class="pa-0 pb-1">
                        #{{ cate }}
                      </v-card-text>
                    </v-card>
                  </v-hover>
                </v-list-item>
              </v-list>
            </v-container>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    
  </v-container>
</template>

<script>
import http from '../http-common'

export default {
  data: () => ({
    map: "",
    storeList : [],
    distance : "100",
    timer : null,
    timerDelay : 500,
    markers : [],
    circle : "",
    curDot : "",

  }),
  created() {
    if (!(window.kakao && window.kakao.maps)) this.addScript()
  },
  mounted() {
    this.drawMap()
  },
  methods: {
    addScript() {
      const script = document.createElement('script') /* global kakao */
      script.onload = () => kakao.maps.load(this.initMap)
      script.src =
        'http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=053dd3145f395e73cbb5211bedf3e97f'
      document.head.appendChild(script)
    },
    drawMap() {
      var mapContainer = document.getElementById('map') // 지도를 표시할 div 
      var mapOption = { 
        center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
        level: 4 // 지도의 확대 레벨 
      }; 

      this.map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

      // 중심 좌표 움직일 때마다
      kakao.maps.event.addListener(this.map, 'center_changed',() => {
        
        clearTimeout(this.timer);
        this.timer = setTimeout(() =>{
          this.calNearStore(this.map.getCenter().getLat(),this.map.getCenter().getLng())
        }, this.timerDelay);

      });

      // HTML5의 geolocation으로 사용할 수 있는지 확인합니다 
      if (navigator.geolocation) {
    
        // GeoLocation을 이용해서 접속 위치를 얻어옵니다
        navigator.geolocation.getCurrentPosition(position => {
        
        var lat = position.coords.latitude, // 위도
            lon = position.coords.longitude; // 경도
        
        var locPosition = new kakao.maps.LatLng(lat, lon) // 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다
        var message = '<div style="padding:5px;">여기에 계신가요?!</div>'; // 인포윈도우에 표시될 내용입니다
        
        // 마커와 인포윈도우를 표시합니다
        this.displayCurMarker(locPosition, message);
            
      });
    
      } else { // HTML5의 GeoLocation을 사용할 수 없을때 마커 표시 위치와 인포윈도우 내용을 설정합니다
    
        var locPosition = new kakao.maps.LatLng(33.450701, 126.570667)    
        var message = 'geolocation을 사용할수 없어요..'
        
        this.displayCurMarker(locPosition, message);
      }
    },
    displayCurMarker(locPosition, message) {

      // var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 
      var imageSrc = "../assets/storeTemp.png"; 
      var imageSize = new kakao.maps.Size(24, 35); 
    
      // 마커 이미지를 생성합니다    
      var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 

      // 마커를 생성합니다
      var marker = new kakao.maps.Marker({  
        map: this.map, 
        position: locPosition,
        image : markerImage
      }); 
    
      // var iwContent = message // 인포윈도우에 표시할 내용
      // var iwRemoveable = true;

      // // 인포윈도우를 생성합니다
      // var infowindow = new kakao.maps.InfoWindow({
      //   content : iwContent,
      //   removable : iwRemoveable
      // });
    
      // // 인포윈도우를 마커위에 표시합니다 
      // infowindow.open(this.map, marker);
    
      // 지도 중심좌표를 접속위치로 변경합니다
      this.map.setCenter(locPosition);      
    },
    calNearStore(curLat, curLng){
      this.deleteMarkers()
      if(this.circle != "")
        this.deleteCircle()
      if(this.curDot != "")
        this.deleteCurDot()

      let form = new FormData()
      form.append('latitude', curLat)
      form.append('longitude', curLng)
      form.append('distance',Number(this.distance)/1000)

      http
        .post('api/SearchNearbyStore', form)
        .then(response => {
          this.storeList = response.data
          this.addMarkers()
          this.addCircle(curLat,curLng)
          this.addCurDot(curLat,curLng)
        })
        .catch(err => {
          console.log(err)
        })
    },
    addMarkers(){

      var storeList = this.storeList
      var imageSrc = "https://i1.daumcdn.net/dmaps/apis/n_local_blit_04.png"
      var imageSize =new kakao.maps.Size(31, 35);
      var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 

      for (let index = 0; index < storeList.length; index++) {

        // 위치
        var locPosition = new kakao.maps.LatLng(storeList[index].latitude, storeList[index].longitude)
        var marker = new kakao.maps.Marker({
          position: locPosition,
        }); 

        //인포윈도우
        // var iwContent = storeList[index].store_name
        // var iwRemoveable = true;
        // var infowindow = new kakao.maps.InfoWindow({
        //   content : iwContent,
        //   removable : iwRemoveable
        // })
        // infowindow.open(this.map, marker);

        marker.setMap(this.map);
        marker.setImage(markerImage)
        this.markers.push(marker);

        
      }
      
    },
    addCircle(curLat,curLng){
      this.circle = new kakao.maps.Circle({
        center : new kakao.maps.LatLng(curLat,curLng),  // 원의 중심좌표 입니다 
        radius: this.distance, // 미터 단위의 원의 반지름입니다 
        strokeOpacity: 0, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
        // strokeWeight: 5, // 선의 두께입니다 
        // strokeColor: '#75B8FA', // 선의 색깔입니다
        // strokeStyle: 'dashed', // 선의 스타일 입니다
        fillColor: '#CFE7FF', // 채우기 색깔입니다
        fillOpacity: 0.4  // 채우기 불투명도 입니다   
      }); 
     

      // 지도에 원을 표시합니다 
      this.circle.setMap(this.map); 
    },
    addCurDot(curLat,curLng){
      this.curDot = new kakao.maps.Circle({
        center : new kakao.maps.LatLng(curLat,curLng),  // 원의 중심좌표 입니다 
        radius: 4, // 미터 단위의 원의 반지름입니다 
        strokeOpacity: 0, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
        // strokeWeight: 5, // 선의 두께입니다 
        // strokeColor: '#75B8FA', // 선의 색깔입니다
        // strokeStyle: 'dashed', // 선의 스타일 입니다
        fillColor: '#FF0000', // 채우기 색깔입니다
        fillOpacity: 1  // 채우기 불투명도 입니다   
      }); 
     

      // 지도에 원을 표시합니다 
      this.curDot.setMap(this.map); 
    },
    deleteMarkers(){
      for (var i = 0; i < this.markers.length; i++) {
        this.markers[i].setMap(null);
      }
      this.markers = []    
    },
    deleteCircle(){
      this.circle.setMap(null); 
      // this.circle = ""
    },
    deleteCurDot(){
      this.curDot.setMap(null); 
      // this.curDot = ""
    },
    enterStoreCard(index){

      var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"
      var imageSize = new kakao.maps.Size(24, 35); 
      var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 
      
      this.markers[index].setImage(markerImage)

      // marker.setImage(markerImage);
      // var locPosition = new kakao.maps.LatLng(lat, lng)
      // this.map.setCenter(locPosition);
      // this.map.setLevel(2)
    },
    leaveStoreCard(index){

      var imageSrc = "https://i1.daumcdn.net/dmaps/apis/n_local_blit_04.png"
      var imageSize =new kakao.maps.Size(31, 35);
      var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 
      
      this.markers[index].setImage(markerImage)

      // marker.setImage(markerImage);
      // var locPosition = new kakao.maps.LatLng(lat, lng)
      // this.map.setCenter(locPosition);
      // this.,map.setLevel(2)
    },
    changeDistance(){
      var centerLat = this.map.getCenter().getLat()
      var centerLng = this.map.getCenter().getLng()
      this.calNearStore(centerLat,centerLng)
    }

  },

  }
</script>

<style scoped>
</style>
