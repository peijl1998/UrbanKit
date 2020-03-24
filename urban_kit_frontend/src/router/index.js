import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/views/HomePage'
import Analysis from '@/views/Analysis'
import NotFound from '@/views/NotFound'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/analysis',
      name: 'Analysis',
      component: Analysis
    },
    {
      path: '/error',
      name: 'NotFound',
      component: NotFound
    }
  ]
})
