import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import ScholarshipMain from '@/components/ScholarshipMain'
import ScholarshipAdminMain from '@/components/admin/ScholarshipAdminMain'
import Notify from '@/components/Notify'
import SendNotify from '@/components/admin/SendNotify'
import ApplyInfoSettings from '@/components/admin/ApplyInfoSettings'
import ScoreRuleSettings from '@/components/admin/ScoreRuleSettings'
import MaterialSettings from '@/components/admin/MaterialSettings'
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
      /**
       * Router for common users
       */
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
      /**
       * Router for admins
       */
      path: '/admin',
      component: ScholarshipAdminMain,
      meta: {
        needLogin: true
      },
      children: [
        {
          path: 'view_notify',
          component: Notify
        },
        {
          path: 'apply_list',
          component: ApplyList
        },
        {
          path: 'notify',
          component: SendNotify
        },
        {
          path: 'apply_info_settings',
          component: ApplyInfoSettings
        },
        {
          path: 'apply_score_rule_settings',
          component: ScoreRuleSettings
        },
        {
          path: 'apply_material_settings',
          component: MaterialSettings
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
    },
    {
      path: '*',
      redirect: '/'
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
