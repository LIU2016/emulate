import Vue from 'vue'
import Vuex from 'vuex'
import Login from '@/components/user/login'

Vue.use(Vuex)

export default new Vuex.Store({
  /* 定义模块的 */
  modules: {
    Login: Login
  },

  /* 定义全局的 */
  state: {
    job: 'web'
  },

  getters: {
    jobTitle (state) {
      return state.job + 'developer'
    }
  }
})
