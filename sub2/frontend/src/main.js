import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import infiniteScroll from "vue-infinite-scroll";
import router from "./router";
import store from "./store";
import VueAxios from 'vue-axios'
import VueAuthenticate from 'vue-authenticate'
import axios from 'axios';
import 'animate.css'
import 'fullpage-vue/src/fullpage.css'
import VueFullpage from 'fullpage-vue'

var VueCookie = require('vue-cookie');

Vue.use(VueFullpage)
Vue.use(VueAxios, axios)
Vue.use(VueCookie);
Vue.config.productionTip = false;
Vue.use(infiniteScroll);
Vue.use(VueAuthenticate, {
    baseUrl: 'http://localhost:8000', // Your API domain

    providers: {
        github: {
            clientId: '',
            redirectUri: 'http://localhost:8080' // Your client app URL
        }
    }
})

new Vue({
    vuetify,
    router,
    store,
    render: h => h(App)
}).$mount("#app");