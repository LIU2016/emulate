import Vue from 'Vue'
import Vuex from 'Vuex'

Vue.use(Vuex)

const state = {
  count: 0
}

const actions = {

  increment: ({
    commit
  }) => commit('increment'),
  decrement: ({
    commit
  }) => commit('decrement')
}

const mutations = {

  increment (state) {
    state.count = state.count + 1
  },

  decrement (state) {
    state.count = state.count - 1
  }
}

const getters = {
  count: state => state.count
}

export default new Vuex.Store({
  state,
  mutations,
  actions,
  getters
})
