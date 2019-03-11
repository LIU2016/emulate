import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld.vue'
import VUEXSTORE from '@/components/Counter.vue'
import HI from '@/components/Hi'
import Login from '@/components/user/login/login.vue'

Vue.use(Router)

export default new Router({
  routes: [{
    path: '/',
    name: 'HelloWorld',
    component: HelloWorld
  },
  {
    path: '/hi',
    name: 'hi',
    component: HI
  },
  {
    path: '/vuex',
    name: 'vuexstore',
    component: VUEXSTORE
  },
  {
    path: '/login',
    name: 'userlogin',
    component: Login
  }
  ]
})
