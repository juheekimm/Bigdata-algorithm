<template>
    <v-btn v-if="$cookie.get('token') == null" @click.stop="loginDialog = true" rounded>로그인
    <v-dialog v-model="loginDialog" max-width="290">
      <v-card>
        <v-card-title>
          <span class="headline">Login</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" class="px-0">
                <v-text-field placeholder="ID" solo hide-details v-model="id"></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" class="px-0">
                <v-text-field type="password" placeholder="Password" solo hide-details v-model="password"></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" class="px-0">
                <v-btn color="primary" large block @click="login"><b>Login</b></v-btn>
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
    </v-btn>
    
</template>

<script>
import http from '../http-common'

export default {
  data: () => ({
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
    id: "",
    password : "",
  }),
  computed: {
    
  },
  mounted() {
  },
  beforeDestroy() {
  },

  methods: {
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
      if(nickname.length < 2)
        return "닉네임을 2자리이상 작성해주세요"
      else if(nickname.length > 5)
        return "닉네임은 최대 5자 까지 가능합니다."
      else 
        return true
    },   
    test(){
      // this.$cookie.set('token', 'gg' , { expires: '60s' });
      console.log(this.$cookie.get('csrftoken'))
      // window.location.reload();
      // this.$cookie.delete('token')
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
            alert("회원가입에 성공헀습니다.")
            this.joinDialog = false
          })
          .catch((error) => {
            // userName 중복
            if(error.response.data.username != undefined){
              alert("중복된 ID입니다.")
              this.username = ""
            }
            // email 중복
            else if(error.response.data.email != undefined){
              alert("중복된 email입니다.")
              this.email = ""
            }

            console.log(error)

        })
      }else{ // 조건이 안되면
        alert("양식을 다 지켜주세요.")
      }

    },
    login(){
      let form = new FormData()
      form.append('username', this.id)
      form.append('password', this.password)

      http
        .post('/auth/token/',form)
        .then(response => {
          console.log(response)
          console.log(response.data)
          this.$cookie.set('token', response.data.token , { expires: '30m' });
          window.location.reload()
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
    },
  }
};
</script>
