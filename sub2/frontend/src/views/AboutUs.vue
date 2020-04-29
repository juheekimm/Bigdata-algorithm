<template>
  <v-container class="px-5" fill-height>
    <v-layout>      
      <v-flex md4 xs12 v-for="(member,index) in members" :key="index+'ss'"  class="animated flipInY pa-5">
        <v-sheet
          :color="member.color"
          width="100%"
          height="100%"
          class="card"
          >
          <v-row
            style="height:50%"
            align="end"
            justify="center"
            >
            <div>
              <div style="text-align-last: center;"  class="Do fs50">
                {{member.name}}
              </div>
              <div class="Do fs50">
                {{member.position}}
              </div>
              <div class="Do fs20" style="text-align-last: center;">
                {{member.role}}
              </div>
              <div style="text-align-last: center;" class="mb-5">
                {{member.email}}
              </div>
            </div>
          </v-row>
          <v-row
            style="height:50%"
            align="center"
            justify="center"
            >
            <div>
              <div v-for="(work,index) in member.works" :key="index+member.name" style="text-align-last: center;" class="Nanum">
                {{work}}
              </div>
            </div>
          </v-row>
        </v-sheet>
      </v-flex>
     
      

    </v-layout>
  </v-container>
</template>

<script>
export default {
  data: () => ({
      members : [
        {
          name: "김태민",
          position: "Front/Back",
          role : "GIT MASTER",
          color: "#FFFFA1",
          email: "taeminkim23@gmail.com",
          works: [
            "Vue.js, Django",
            "자동완성기능",
            "지도 기반 서비스(Kakao Map)",
            "JWT, REST",
            "Design",
            "AWS"
          ]
        },
        {
          name : "이재혁",
          position : "Back/Algorithm",
          role : "READER",
          color : "#B2CCFF",
          email : "jason07999@naver.com",
          works: [
            "Django",
            "음식점 기반 알고리즘(TF-IDF)",
            "DB모델링",
            "데이터 가공",
            "AWS"
          ]
        },
        {
          name: "김주희",
          position: "Back/Algorithm",
          role : "JIRA MASTER",
          color: "#D1B2FF",
          email: "yylcd9999@naver.com ",
          works : [
            "Django",
            "유저 기반 알고리즘",
            "음식점 기반 알고리즘(Matrix Factorization)", 
            "로그인/회원가입(JWT)"
          ]
        },
      ],
  })
}
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic&Do+Hyeon&family=Noto+Serif+KR:wght@300;400;900&family=Song+Myung&display=swap');
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
.Nanum {
  font-family: 'Nanum Gothic', sans-serif;
}
.fs70 {
  font-size: 70px;
}
.fs50 {
  font-size: 50px;
}
.fs20 {
  font-size: 20px;
}
</style>