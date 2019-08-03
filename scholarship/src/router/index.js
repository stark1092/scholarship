import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import ScholarshipMain from '@/components/ScholarshipMain'
import Notify from '@/components/Notify'
import ApplyMain from '@/components/ApplyMain'
import ApplyList from '@/components/ApplyList'
import HelloWorld from '@/components/HelloWorld'
import StucsLogin from '@/components/StucsLogin'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Login,
      meta: {
        title: '系统登陆'
      }
    },
    {
      path: '/home',
      component: ScholarshipMain,
      meta: {
        needLogin: true
      },
      children: [
        {
          path: 'notify',
          component: Notify
        },
        {
          path: 'apply',
          component: ApplyMain
        },
        {
          path: 'view_apply',
          component: ApplyMain
        },
        {
          path: 'apply_list',
          component: ApplyList
        }
      ]
    },
    {
      path: '/vue-default',
      component: HelloWorld
    },
    {
      path: '/userlogin_stucs_cb',
      component: StucsLogin
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }
  if (to.meta.needLogin && window.sessionStorage.token == null) {
    next({
      path: '/',
      query: {message: '未登录，现在跳转到登录页面'}
    })
  }
  next()
})

export default router
