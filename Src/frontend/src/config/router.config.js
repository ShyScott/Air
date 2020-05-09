// eslint-disable-next-line
import { UserLayout, BasicLayout, RouteView, BlankLayout, PageView } from '@/layouts'

export const asyncRouterMap = [

  {
    path: '/',
    name: 'index',
    component: BasicLayout,
    meta: { title: '首页' },
    children: [
      // account
      {
        path: '/account',
        component: RouteView,
        redirect: '/account/settings',
        name: 'account',
        hidden: true,
        meta: { title: '个人页', icon: 'user', keepAlive: true },
        children: [
          {
            path: '/account/settings',
            name: 'settings',
            component: () => import('@/views/account/settings/Index'),
            meta: { title: '个人设置', hideHeader: true, permission: [ 'user' ] },
            redirect: '/account/settings/base',
            hideChildrenInMenu: true,
            children: [
              {
                path: '/account/settings/base',
                name: 'BaseSettings',
                component: () => import('@/views/account/settings/BaseSetting'),
                meta: { title: '基本设置', hidden: true, permission: [ 'user' ] }
              },
              {
                path: '/account/settings/security',
                name: 'SecuritySettings',
                component: () => import('@/views/account/settings/Security'),
                meta: { title: '安全设置', hidden: true, keepAlive: true, permission: [ 'user' ] }
              },
              {
                path: '/account/settings/custom',
                name: 'CustomSettings',
                component: () => import('@/views/account/settings/Custom'),
                meta: { title: '个性化设置', hidden: true, keepAlive: true, permission: [ 'user' ] }
              },
              {
                path: '/account/settings/binding',
                name: 'BindingSettings',
                component: () => import('@/views/account/settings/Binding'),
                meta: { title: '账户绑定', hidden: true, keepAlive: true, permission: [ 'user' ] }
              },
              {
                path: '/account/settings/notification',
                name: 'NotificationSettings',
                component: () => import('@/views/account/settings/Notification'),
                meta: { title: '新消息通知', hidden: true, keepAlive: true, permission: [ 'user' ] }
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*', redirect: '/404', hidden: true
  }
]

/**
 * Router dedicated for Student
 */
export const studentRoutes = [
  {
    path: 'mainpage',
    name: 'Index',
    meta: { title: 'Main', icon: 'smile' },
    component: () => import('@/views/student/index')
  },
  {
    path: 'team',
    name: 'Team',
    meta: { title: 'Team Management', icon: 'team' },
    component: () => import('@/views/student/Team/TeamManagement')
  },
  {
    path: 'assessment',
    name: 'Assessment',
    meta: { title: 'Assessment Management', icon: 'like' },
    component: () => import('@/views/student/Assessment/Assessment')
  },
  {
    path: `assessment/assessSubmission/:courseId`,
    name: 'AssessSubmission',
    component: () => import('@/views/student/Assessment/AssessSubmission'),
    meta: { title: 'Assess Submission' },
    hidden: true
  },
  {
    path: `team/viewInvitation`,
    name: 'ViewInvitation',
    component: () => import('@/views/student/Team/ViewInvitation'),
    meta: { title: 'View Invitation' },
    hidden: true
  }
]

/**
 * Router dedicated for Teacher
 */
export const teacherRoutes = [
  {
    path: 'mainpage',
    name: 'Index',
    component: () => import('@/views/teacher/index'),
    meta: { title: 'Main', icon: 'crown' }
  },
  {
    path: 'course',
    name: 'CourseManagement',
    component: () => import('@/views/teacher/course/CourseManagement'),
    meta: { title: 'Course Management', icon: 'solution' }
  },
  {
    path: 'course/addCourse',
    name: 'AddCourse',
    component: () => import('@/views/teacher/course/AddCourse'),
    meta: { title: 'Course Management' },
    hidden: true
  },
  {
    path: 'contribution',
    name: 'ViewContribution',
    component: () => import('@/views/teacher/contribution/ViewContribution'),
    meta: { title: 'View Contribution', icon: 'like' }
  },
  {
    path: 'submission',
    name: 'SubmissionManagement',
    component: () => import('@/views/teacher/submission/SubmissionManagement'),
    meta: { title: 'Submission Management', icon: 'upload' }
  },
  {
    path: 'team',
    name: 'TeamManagement',
    component: () => import('@/views/teacher/team/TeamManagement'),
    meta: { title: 'Team Management', icon: 'team' }
  },
  {
    path: `team/formConfirmation/:courseId`,
    name: 'FormConfirmation',
    component: () => import('@/views/teacher/team/FormConfirmation'),
    meta: { title: 'Team Form Confirmation' },
    hidden: true
  }

]

/**
 * 基础路由
 * @type { *[] }
 */
export const constantRouterMap = [
  {
    path: '/user',
    component: UserLayout,
    redirect: '/user/login',
    hidden: true,
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/Login')
      }
    ]
  },

  {
    path: '/404',
    component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/404')
  }
]
