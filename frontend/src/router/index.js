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

const beforeEachHook = (to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }
  if (to.meta.needLogin && window.sessionStorage.token == null) {
    next({
      path: '/',
      query: { message: '未登录，现在跳转到登录页面' }
    })
  } else if (to.meta.needAdmin && window.sessionStorage.user_type !== '2') {
    next({
      path: '/home'
    })
  } else next()
}

const userTitle = '奖学金系统'
const adminTitle = '奖学金系统-管理后台'
const userMeta = {
  needLogin: true,
  title: userTitle
}
const adminMeta = {
  needLogin: true,
  needAdmin: true,
  title: adminTitle
}

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
      meta: userMeta,
      children: [
        {
          path: 'notify',
          component: Notify,
          meta: userMeta
        },
        {
          path: 'apply',
          component: ApplyMain,
          meta: userMeta
        },
        {
          path: 'view_apply',
          component: ApplyMain,
          meta: userMeta
        },
        {
          path: 'apply_list',
          component: ApplyList,
          meta: userMeta
        }
      ]
    },
    {
      /**
       * Router for admins
       */
      path: '/admin',
      component: ScholarshipAdminMain,
      meta: adminMeta,
      children: [
        {
          path: 'view_notify',
          component: Notify,
          meta: adminMeta
        },
        {
          path: 'apply_list',
          component: ApplyList,
          meta: adminMeta
        },
        {
          path: 'notify',
          component: SendNotify,
          meta: adminMeta
        },
        {
          path: 'apply_info_settings',
          component: ApplyInfoSettings,
          meta: adminMeta
        },
        {
          path: 'apply_score_rule_settings',
          component: ScoreRuleSettings,
          meta: adminMeta
        },
        {
          path: 'apply_material_settings',
          component: MaterialSettings,
          meta: adminMeta
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

router.beforeEach(beforeEachHook)

export default router
