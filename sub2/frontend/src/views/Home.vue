<template>
  <div class="fullpage-container">
      <div class="fullpage-wp" v-fullpage="opts">

        <div class="page-1 page">
          <p class="Do fs70" v-animate="{value: 'bounceInDown',delay: 0}">세명맛집</p>
          <p class="Do fs50" v-animate="{value: 'bounceInDown',delay: 100}">
            <span style="color : red">세</span>상 유<span style="color : red">명</span>한 <span style="color : red">맛집 모두다!</span>
          </p>
          <p class="Noto fs40" v-animate="{value: 'bounceInDown',delay: 200}">★우리 세명이 이걸 만든 겁니다★</p>
        </div>

        <div class="page-2 page" style="color: black;">
          <p class="Do fs50" v-animate="{value: 'zoomIn',delay: 0}">
            <v-icon class="fs70" style="color:#368AFF">mdi-account</v-icon>사용자 맞춤 기능<v-icon class="fs70" style="color:#368AFF">mdi-account</v-icon>
          </p>
          <p class="Noto fs40 mt-5" v-animate="{value: 'zoomIn',delay: 250}" >
            회원가입 후, 유저 프로필을 작성하시면
          </p>
          <p class="Noto fs40 mt-5" v-animate="{value: 'zoomIn',delay: 250}" >
            사용자 맞춤 맛집을 알 수 있습니다.
          </p>
          <p class="Noto fs40" v-animate="{value: 'zoomIn',delay: 500}">
          </p>
        </div>

        <div class="page-3 page">
          <p class="Do fs50" v-animate="{value: 'zoomIn',delay: 0}">
            <v-icon class="fs70" style="color:red">mdi-map-marker</v-icon>위치기반 서비스<v-icon class="fs70" style="color:red">mdi-map-marker</v-icon>
          </p>
          <p class="Noto fs40" v-animate="{value: 'zoomIn',delay: 300}">
            현재 위치 주변에 있는 음식점을 검색해보세요!
          </p>
          <p class="Noto fs40" v-animate="{value: 'zoomIn',delay: 500}">
            지도를 이용해 음식점 검색이 가능합니다!
          </p>
        </div>

        <div class="page-4 page" style="color: black;">
          <p class="Do fs50" v-animate="{value: 'zoomIn',delay: 0}">
            검색기능
          </p>
          <p class="Noto fs40" v-animate="{value: 'zoomIn',delay: 300}">
            자동완성기능을 이용해 빠르게 검색해보세요.
          </p>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  created : function(){
    this.$vuetify.goTo(0)
  },
  data () {
      return {
        opts: {
          start: 0,
          dir: 'v',
          loop: false,
          duration: 300,
          beforeChange: function (prev, next) {
            // console.log('before', prev, next)
          },
          afterChange: function (prev, next) {
            // console.log('after', prev, next)
          }
        }       
      }
    },
  methods : {
    
  },
};
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Do+Hyeon&family=Noto+Serif+KR:wght@300;400;900&family=Song+Myung&display=swap');
.Song {
  font-family: 'Song Myung', serif;
}
.Noto {
  font-family: 'Noto Serif KR', serif;
}
.Do {
  font-family: 'Do Hyeon', sans-serif;
}
.fs70 {
  font-size: 70px;
}
.fs50 {
  font-size: 50px;
}
.fs40 {
  font-size: 40px;
}
.image-container{
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }
.fullpage-container {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
}
.page {
    display: block;
    text-align: center;
    color: #eee;
}
.page-1 {
  padding-top: 130px;
  background: #1bbc9b;
}
.page-2 {
  padding-top: 150px;
  background: #E8D9FF
}
.page-3 {
  padding-top: 150px;
  background: #aabbcc;
}
.page-4 {
  padding-top: 150px;
  background: #FFC19E;
}
</style>