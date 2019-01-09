import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
import VueAxios from "vue-axios";
import config from "./config.js"
import "./plugins/iview.js";

Vue.config.productionTip = false;
Vue.config.devtools = true;
Vue.use(VueAxios, axios);
Vue.prototype.$config = config

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
