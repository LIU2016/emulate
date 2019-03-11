/* eslint-disable spaced-comment */
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import App1 from './App'
import router from './router'
// eslint-disable-next-line spaced-comment
//import Loading from './components/loading/Loading.vue'
//import store from './store/store'
import store from './store'

Vue.config.productionTip = true

Vue.use(Vuex)
//Vue.use(Loading)

/* eslint-disable no-new */
new Vue({
  el: '#app1',
  router: router,
  store: store,
  components: {
    App1
  },
  template: '<App1></App1>'
})
