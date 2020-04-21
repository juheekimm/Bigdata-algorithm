<template>
  <v-app-bar id="app-toolbar" app flat color="blue lighten-1">
    <v-btn @click="test">test</v-btn>
    
    <v-btn v-if="responsive" dark icon @click.stop="onClickDrawer">
      <v-icon>mdi-view-list</v-icon>
    </v-btn>
    <v-spacer></v-spacer>
    <v-btn text @click.stop="loginDialog = true">로그인해주세요.</v-btn>
    <v-dialog v-model="loginDialog" max-width="290">
      <v-card>
        <v-card-title>
          <span class="headline">Login</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field placeholder="ID" solo></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-text-field placeholder="Password" solo ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-btn color="primary" large block><b>Login</b></v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="joinDialog = !joinDialog" small> 아이디가 없으신가요?회원가입하러 가기</v-btn>
        </v-card-actions> 
      </v-card>
    </v-dialog>
    <v-dialog
        v-model="joinDialog"
        max-width="500px"
      >
        <v-card>
          <v-card-title>
            <span class="headline">회원가입</span>
          </v-card-title>
          <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" class="pa-0">
                <v-text-field label="ID*" v-model="username" required :rules="[idHintMethod]"></v-text-field>
              </v-col>
              <v-col cols="12" class="pa-0">
                <v-text-field label="Email*" v-model="email" required :rules="[emailHintMethod]"></v-text-field>
              </v-col>
              <v-col cols="12" class="pa-0">
                <v-text-field id="pw" label="Password*" type="password" v-model="password1" required :rules="[passwordHintMethod]"></v-text-field>
              </v-col>
              <v-col cols="12" class="pa-0">
                <v-text-field label="password확인" type="password" v-model="password2" required :rules="[vertifyPassword]"></v-text-field>
              </v-col>
              <v-col cols="12" class="pa-0">
                <v-text-field label="닉네임" v-model="nickname" required :rules="[nicknameHintMethod]"></v-text-field>
              </v-col>
              <v-col cols="12" class="pa-0">
                <v-radio-group v-model="gender" row>
                  <span>성별</span>
                  <v-spacer></v-spacer>
                  <v-radio label="남" value="남"></v-radio>
                  <v-radio label="여" value="여"></v-radio>
                </v-radio-group>
              </v-col>
              <v-col cols="12" class="pa-0">
                <v-select
                  :items="selectorItems()"
                  label="연령"
                  v-model="age"
                ></v-select>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
          <v-card-actions>
            <v-layout justify-end>
              <v-btn color="primary" text @click="joinDialog = !joinDialog">Close</v-btn>
              <v-btn color="primary" @click="signup">signup</v-btn>
            </v-layout>
          </v-card-actions>
        </v-card>
      </v-dialog>
  </v-app-bar>
</template>

<script>
import { mapMutations, mapState } from "vuex";
import http from '../http-common'
import axios from "axios"

export default {
  data: () => ({
    responsive: false,
    loginDialog: false,
    joinDialog: false,
    username: "",
    email: "",
    password1 : "",
    password2 : "",
    gender: "남",
    age: "2000",
    nickname:"",
    passwordError:true,
    rules: {
          required: value => !!value || '반드시 입력해주세요.',
          counter: value => value.length <= 20 || '20자가 넘었습니다.',
          email: value => {
            const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            return pattern.test(value) || '이메일 형식에 맞지 않습니다.'
          },
    },
  }),
  computed: {
    ...mapState("app", ["drawer"])
  },
  mounted() {
    this.onResponsiveInverted();
    window.addEventListener("resize", this.onResponsiveInverted);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResponsiveInverted);
  },

  methods: {
    ...mapMutations("app", ["setDrawer"]),
    onClickDrawer() {
      this.setDrawer(!this.drawer);
    },
    onResponsiveInverted() {
      if (window.innerWidth < 1800) {
        this.responsive = true;
      } else {
        this.responsive = false;
      }
    },
    selectorItems(){
      var list = []
      var curYear = new Date().getFullYear()
      for (let index = curYear-100 ; index <= curYear; index++) {
        list.push(index)
      }
      this.age = 2000
      return list
    },
    vertifyPassword(){
     var pass = this.password2
      if(pass.length == 0 || this.password1 != this.password2)
        return '비밀번호가 맞지 않습니다.'
      else
        return true
    },
    passwordHintMethod(){
      var pass = this.password1
      var engNum = /^[a-zA-Z0-9]*$/;
      var num = /^[0-9]*$/;
      var eng = /^[a-zA-Z]*$/; 
      if(pass.length < 8)
        return "비밀번호를 최소 8자이상 작성해주세요"
      else if(pass.lenght > 20)
        return "비밀번호를 최대 20자 까지 가능합니다."
      else if(! engNum.test(pass))
        return "영어와 숫자만 입력해주세요"
      else if(num.test(pass) || eng.test(pass))
        return "영어와 숫자를 혼합해주세요"
      else 
        return true
    },
    idHintMethod(){
      var id = this.username
      if(id.length < 6)
        return "아이디를 6자리이상 작성해주세요"
      else if(id.lenght > 15)
        return "아이디는 최대 15자 까지 가능합니다."
      else 
        return true
    },
    emailHintMethod(){
      const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      const email = this.email
      if(email.length == 0)
        return "이메일을 입력해주세요"
      else if(!pattern.test(email))
        return "이메일이 형식에 맞지 않습니다."
      else
        return true
    },
    nicknameHintMethod(){
      const nickname = this.nickname
      if(nickname.length < 3)
        return "닉네임을 3자리이상 작성해주세요"
      else if(nickname.lenght > 6)
        return "닉네임은 최대 6자 까지 가능합니다."
      else 
        return true
    },   
    test(){
      return false
    },
    signup(){
      if(this.idHintMethod() == true && this.vertifyPassword() == true && this.passwordHintMethod()== true && this.emailHintMethod()==true && this.nicknameHintMethod() ==true){
        let form = new FormData()
        form.append('username', this.username)
        form.append('email', this.email)
        form.append('password1', this.password1)
        form.append('password2', this.password2)
        form.append('gender', this.gender)
        form.append('age', this.age)
        form.append('nickname', this.nickname)

        http
          .post('/auth/regi',form)
          .then(response => {
            // console.log(response.data)
            console.log(response)
            console.log(response.data)
            alert("회원가입에 성공헀습니다.")
          })
          .catch((error) => {
            // userName 중복
            if(error.response.data.username != undefined){

              console.log(error.response.data.username)
            }

            // email 중복
            if(error.response.data.email != undefined){
              console.log(error.response.data.email)
            }

            if(error.response.data.password1 != undefined){
              this.passwordError = error.response.data.password1[0]
            }

            console.log(error.response.data)

        })
      }else{ // 조건이 안되면
        alert("양식을 다 지켜주세요.")
      }

    },
  }
};
</script>
