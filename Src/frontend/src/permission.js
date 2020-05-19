import Vue from 'vue'
import router from './router'
import store from './store'

import NProgress from 'nprogress' // progress bar
import '@/components/NProgress/nprogress.less' // progress bar custom style
import notification from 'ant-design-vue/es/notification'
import { setDocumentTitle, domTitle } from '@/utils/domUtil'
import { ACCESS_TOKEN } from '@/store/mutation-types'

NProgress.configure({ showSpinner: false }) // NProgress Configuration

const whiteList = ['login'] // no redirect whitelist

router.beforeEach((to, from, next) => {
  NProgress.start() // start progress bar
  to.meta && (typeof to.meta.title !== 'undefined' && setDocumentTitle(`${to.meta.title} - ${domTitle}`))
  if (Vue.ls.get(ACCESS_TOKEN)) {
    /* has token */
    if (store.getters.nickname === '') {
      store
        .dispatch('GetInfo')
        .then(() => {
          store.dispatch('GenerateRoutes', store.getters.isTeacher).then(() => {
            // 根据权限生成并添加可访问的路由表
            router.addRoutes(store.getters.addRouters)

            let path = to.path
            if (path === '/' || path === '/user/login') path = '/mainpage'
            next({ path })
          })
        })
        .catch(() => {
          notification.error({
            message: 'Error',
            description: 'Failed to get your profile'
          })
          store.dispatch('Logout').then(() => {
            next({ path: '/user/login' })
          })
        })
    } else {
      if (to.path === '/' || to.path === '/user/login') {
        next({ path: '/mainpage' })
        NProgress.done()
      } else {
        next()
      }
    }
  } else {
    if (whiteList.includes(to.name)) {
      // 在免登录白名单，直接进入
      next()
    } else {
      next({ path: '/user/login' })
      NProgress.done() // if current page is login will not trigger afterEach hook, so manually handle it
    }
  }
})

router.afterEach(() => {
  NProgress.done() // finish progress bar
})
