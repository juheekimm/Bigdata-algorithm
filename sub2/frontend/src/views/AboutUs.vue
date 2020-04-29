<template>
  <v-container class="px-5" fill-height>
    <v-layout>
      <v-flex sm4 class="animated flipInY pa-5">
        <v-sheet
            color="#FFFFA1"
            width="100%"
            height="100%"
            class="card"
            >
            <v-row
              class="fill-height"
              align="center"
              justify="center"
              >
              <div>
                <p style="text-align-last: center;" >
                  <v-icon style="font-size:100px" color="pink">mdi-account-question</v-icon>
                </p>
                <div class="display-1">검색된 결과가 없습니다.</div>
              </div>
            </v-row>
          </v-sheet>
      </v-flex>
      <v-flex sm4 class="animated flipInY pa-5">
        <v-sheet
            color="#B2CCFF"
            width="100%"
            height="100%"
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
      </v-flex>
      <v-flex sm4 class="animated flipInY pa-5">
        <v-sheet
            color="#D1B2FF"
            width="100%"
            height="100%"
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
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
export default {
  created : function(){
    
  },
  data () {
      return {
             
      }
    },
  methods : {
    
  },
};
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Do+Hyeon&family=Noto+Serif+KR:wght@300;400;900&family=Song+Myung&display=swap');
.card{
  border-radius: 30px;
}
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
.page-5 {
  padding-top: 150px;
  background: #FFA7A7
}
</style>