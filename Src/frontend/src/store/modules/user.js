import Vue from 'vue'
import { login, getMyInfo } from '@/api/auth'
import { getInfo, logout } from '@/api/login'
import { welcome } from '@/utils/util'
import { ACCESS_TOKEN } from '@/store/mutation-types'

const user = {
  state: {
    token: '',
    name: '',
    welcome: '',
    avatar: '',
    isTeacher: true,
    roles: [],
    info: {},
    id: null
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_NAME: (state, { name, welcome }) => {
      state.name = name
      state.welcome = welcome
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_ROLES: (state, roles) => {
      state.roles = roles
    },
    SET_INFO: (state, info) => {
      state.info = info
    },
    SET_IS_TEACHER: (state, isTeacher) => {
      state.isTeacher = isTeacher
    },
    SET_USER_ID: (state, id) => {
      state.id = id
    }
  },

  actions: {
    // 登录
    Login ({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        login(userInfo).then(response => {
          const token = 'Bearer ' + response.data.access
          // 设置 Vue-ls 存储的 ACCESS_TOKEN 超时时间为 30 分钟
          Vue.ls.set(ACCESS_TOKEN, token, 30 * 60 * 1000)
          commit('SET_TOKEN', token)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 获取用户信息
    GetInfo ({ commit }) {
      return new Promise((resolve, reject) => {
        getInfo().then(response => {
          const { data: { result } } = response

          if (result.role && result.role.permissions.length > 0) {
            const role = result.role
            role.permissions = result.role.permissions
            role.permissions.map(per => {
              if (per.actionEntitySet != null && per.actionEntitySet.length > 0) {
                const action = per.actionEntitySet.map(action => {
                  return action.action
                })
                per.actionList = action
              }
            })
            role.permissionList = role.permissions.map(permission => {
              return permission.permissionId
            })
            commit('SET_ROLES', result.role)
            commit('SET_INFO', result)
          }

          // commit('SET_NAME', { name: result.name, welcome: welcome() })
          commit('SET_AVATAR', result.avatar)

          getMyInfo().then(({ data: user }) => {
            commit('SET_NAME', { name: user.username, welcome: welcome() })
            commit('SET_USER_ID', user.id)
            // commit('SET_AVATAR', user.avatar)
            // If the user identity is a student
            if (user.student_profile) {
              commit('SET_IS_TEACHER', false)
              // Set the layout for students
              // TODO: save student profile
              // save the default UI settings dedicated for student
              commit('SET_SIDEBAR_TYPE', true)
              commit('TOGGLE_THEME', 'dark')
              commit('TOGGLE_LAYOUT_MODE', 'topmenu')
              commit('TOGGLE_FIXED_HEADER', false)
              commit('TOGGLE_FIXED_SIDERBAR', false)
              commit('TOGGLE_CONTENT_WIDTH', 'Fluid')
              commit('TOGGLE_FIXED_HEADER_HIDDEN', true)
              commit('TOGGLE_WEAK', false)
              commit('TOGGLE_COLOR', '#1a8fff')
              commit('TOGGLE_MULTI_TAB', false)
            } else {
              // if the user identity is a teacher
              commit('SET_IS_TEACHER', true)
              commit('SET_SIDEBAR_TYPE', true)
              commit('TOGGLE_THEME', 'dark')
              commit('TOGGLE_LAYOUT_MODE', 'sidemenu')
              commit('TOGGLE_FIXED_HEADER', false)
              commit('TOGGLE_FIXED_SIDERBAR', false)
              commit('TOGGLE_CONTENT_WIDTH', 'Fluid')
              commit('TOGGLE_FIXED_HEADER_HIDDEN', false)
              commit('TOGGLE_WEAK', false)
              commit('TOGGLE_COLOR', '#1a8fff')
              commit('TOGGLE_MULTI_TAB', false)
            }

            resolve(response)
          })
        })
      })
    },

    // 登出
    Logout ({ commit, state }) {
      return new Promise((resolve) => {
        logout(state.token).then(() => {
          resolve()
        }).catch(() => {
          resolve()
        }).finally(() => {
          commit('SET_TOKEN', '')
          commit('SET_ROLES', [])
          Vue.ls.remove(ACCESS_TOKEN)
        })
      })
    }

  }
}

export default user
