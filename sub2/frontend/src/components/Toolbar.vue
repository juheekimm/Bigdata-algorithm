<template>
  <v-app-bar id="app-toolbar" app flat color="blue lighten-1">
    <!-- <v-btn @click="test2" text>set</v-btn> -->
    <!-- <v-btn @click="test2" text>delete</v-btn> -->
    <v-btn v-if="responsive" dark icon @click.stop="onClickDrawer">
      <v-icon>mdi-view-list</v-icon>
    </v-btn>
    <v-spacer></v-spacer>
    <v-img class="mx-2" src="../assets/logo.png" max-height="40"  max-width="40" contain @click="goHome" style="cursor:pointer"></v-img>
    <div class="Do fs40" style="display:inline-block; cursor:pointer" @click="goHome">세명맛집</div>
    <v-spacer></v-spacer>
    <loginDialog v-if="$cookie.get('token') == null"></loginDialog>
    <v-btn v-if="$cookie.get('token') != null" to="/myPage" class="mx-1 cabin" rounded text >myPage</v-btn>
    <v-btn v-if="$cookie.get('token') != null" @click.stop="logout" class="mx-1 cabin" rounded text>Logout</v-btn>
    
  </v-app-bar>
</template>

<script>
import { mapMutations, mapGetters, mapState } from "vuex";
import http from '../http-common'
import loginDialog from './loginDialog'

export default {
  components: {
    loginDialog
  },
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
    id: "",
    password : "",
  }),
  computed: {
    ...mapState("data", ["count","token"]),
    token : () => {
      return this.$cookie.get('token')
    }
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
      if(nickname.length < 2)
        return "닉네임을 2자리이상 작성해주세요"
      else if(nickname.length > 5)
        return "닉네임은 최대 5자 까지 가능합니다."
      else 
        return true
    },   
    
    test2(){
      let form = new FormData()
      form.append('username', 'taemin010')
      form.append('password', 'taemin1234')
  
      
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
    logout(){
      this.$cookie.delete('token')
      window.location.reload()
    },
    goHome(){
      this.$router.push("/")
    }
  }
};
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Do+Hyeon&Cabin&display=swap');
.cabin {
  font-family: 'Cabin', sans-serif;
}
.fs40 {
  font-size: 40px;
}
.Do {
  font-family: 'Do Hyeon', sans-serif;
}
</style>
