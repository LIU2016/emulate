const state = {
  userName: 'lqd'
}

const mutations = {
  CHANG_NAME (state, anotherName) {
    state.userName = anotherName
  }
}

const actions = {
  changeName ({
    commit,
    rootState
  }, anotherName) {
    // eslint-disable-next-line eqeqeq
    if (rootState.job == 'web') {
      commit('CHANG_NAME', anotherName)
    }
  }
}

const getters = {
  localJobTitle (state, getters, rootState, rootGetters) {
    console.log(rootState)
    console.log(rootGetters)
    return rootGetters.jobTitle + '@@' + rootState.job
  },
  testGetters (state) {
    return 'testGetters_' + state.userName
  }
}

export default {

  state,
  mutations,
  actions,
  getters

}
