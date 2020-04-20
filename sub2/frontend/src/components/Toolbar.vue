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
                <v-text-field label="UserName*" v-model="username" required></v-text-field>
              </v-col>
              <v-col cols="12" class="pa-0">
                <v-text-field label="Email*" v-model="email" required :rules="[rules.required, rules.email]"></v-text-field>
              </v-col>
              <v-col cols="12" class="pa-0">
                <v-text-field label="Password*" type="password" v-model="password1" required :rules="[rules.required, rules.counter]"></v-text-field>
              </v-col>
              <v-col cols="12" class="pa-0">
                <v-text-field label="password확인" type="password" v-model="password2" required :rules="[rules.required, rules.counter]"></v-text-field>
              </v-col>
              <v-col cols="12" class="pa-0">
                <span>성별</span>
                <v-radio-group v-model="gender" row>
                  <span>성별</span>
                  <v-spacer></v-spacer>
                  <v-radio label="남" value="남"></v-radio>
                  <v-radio label="여" value="여"></v-radio>
                </v-radio-group>
              </v-col>
              <v-col cols="12" class="pa-0">
                <v-col class="d-flex">
                  <span>연령</span>
                  <v-spacer></v-spacer>
                  <v-select
                    :items="selectorItems()"
                    label="age"
                    v-model="age"
                  ></v-select>
                </v-col>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
          <v-card-actions>
            <v-btn
              color="primary"
              text
              @click="joinDialog = !joinDialog"
            >
              Close
            </v-btn>
            <v-btn
              color="primary"
              text
              @click="signup"
            >
              signup
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  </v-app-bar>
</template>

<script>
import { mapMutations, mapState } from "vuex";
import http from '../http-common'

export default {
  data: () => ({
    responsive: false,
    loginDialog: false,
    joinDialog: false,
    username: "",
    email: "",
    password1 : "",
    password2 : "",
    gender: "",
    age: "",
    rules: {
          required: value => !!value || 'Required.',
          counter: value => value.length <= 20 || 'Max 20 characters',
          email: value => {
            const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            return pattern.test(value) || 'Invalid e-mail.'
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
      return list
    },
    signup(){
      console.log(csrf_token)
      let form = new FormData()
      form.append('username', username)
      form.append('email', input)
      form.append('password1', password1)
      form.append('password2', password2)
      form.append('gender', gender)
      form.append('age', age)
      form.append('csrfmiddlewaretoken',document.head.querySelector("[name=_token]").content)

      http
        .post('api/searchStore', form)
        .then(response => {
          // console.log(response.data)
            console.log(response)
        })
        .catch(err => {
          console.log(err)
        })
    },
    test(){
      console.log(this)
    }
  }
};
</script>
