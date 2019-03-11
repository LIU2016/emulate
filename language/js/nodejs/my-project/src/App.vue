<template>
  <div id="app2">
    <img src="./assets/logo.png">
    <router-view/>
    <router-link to="/" >Hello</router-link>
    <router-link to="/hi">hi</router-link>
    <router-link to="/vuex">vuex</router-link>
    <router-link to="/login">login</router-link>
    <Loading></Loading>
  </div>
</template>

<script>
export default {
  name: 'App1'
}
</script>

<style>
#app2 {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
