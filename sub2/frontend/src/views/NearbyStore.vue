<template>
  <v-container>
    <div id="map" style="width:100%;height:350px;"></div>
  </v-container>
</template>

<script>

export default {
  data: () => ({
    map: "",
  }),
  created() {
    console.log("creatd")
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
        level: 10 // 지도의 확대 레벨 
      }; 

      this.map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

      // HTML5의 geolocation으로 사용할 수 있는지 확인합니다 
      if (navigator.geolocation) {
    
        // GeoLocation을 이용해서 접속 위치를 얻어옵니다
        navigator.geolocation.getCurrentPosition(position => {
        
        var lat = position.coords.latitude, // 위도
            lon = position.coords.longitude; // 경도
        
        var locPosition = new kakao.maps.LatLng(lat, lon) // 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다
        var message = '<div style="padding:5px;">여기에 계신가요?!</div>'; // 인포윈도우에 표시될 내용입니다
        
        // 마커와 인포윈도우를 표시합니다
        this.displayMarker(locPosition, message);
            
      });
    
      } else { // HTML5의 GeoLocation을 사용할 수 없을때 마커 표시 위치와 인포윈도우 내용을 설정합니다
    
        var locPosition = new kakao.maps.LatLng(33.450701, 126.570667)    
        var message = 'geolocation을 사용할수 없어요..'
        
        this.displayMarker(locPosition, message);
      }
    },
    displayMarker(locPosition, message) {

      // 마커를 생성합니다
      var marker = new kakao.maps.Marker({  
          map: this.map, 
        position: locPosition
      }); 
    
      var iwContent = message // 인포윈도우에 표시할 내용
      var iwRemoveable = true;

      // 인포윈도우를 생성합니다
      var infowindow = new kakao.maps.InfoWindow({
        content : iwContent,
        removable : iwRemoveable
      });
    
      // 인포윈도우를 마커위에 표시합니다 
      infowindow.open(this.map, marker);
    
      // 지도 중심좌표를 접속위치로 변경합니다
      this.map.setCenter(locPosition);      
    },    

  },

  }
</script>

<style scoped>
</style>
