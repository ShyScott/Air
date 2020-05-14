import Vue from 'vue'
import { login, logout, getMyInfo } from '@/api/auth'
import { ACCESS_TOKEN } from '@/store/mutation-types'

const user = {
  state: {
    token: '',
    name: '',
    avatar: '',
    isTeacher: true,
    id: null
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_NAME: (state, name) => {
      state.name = name
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
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
          // 这是使用 JWT 时的 Token
          // const token = 'Bearer ' + response.data.access

          // 使用 session 时无需 Token，但是在 router 中无法直接判断 session 的有效性
          // 所以还是设置一个非空串 token，方便在 router.beforeEach() 中判断登录状态
          const token = '1'

          // 设置 Vue-ls 存储的 ACCESS_TOKEN 超时时间为 1 小时（使用 JWT 认证时）
          // Vue.ls.set(ACCESS_TOKEN, token, 60 * 60 * 1000)

          // 使用 session 时不能设置 Vue-ls 的超时
          Vue.ls.set(ACCESS_TOKEN, token)

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
        getMyInfo().then(({ data: user }) => {
          commit('SET_NAME', user.username)
          commit('SET_USER_ID', user.id)
          commit('SET_AVATAR', user.avatar.small)

          // set common app style
          commit('SET_SIDEBAR_TYPE', true)
          commit('TOGGLE_THEME', 'dark')
          commit('TOGGLE_CONTENT_WIDTH', 'Fluid')
          commit('TOGGLE_FIXED_HEADER_HIDDEN', false)
          commit('TOGGLE_WEAK', false)
          commit('TOGGLE_COLOR', '#1a8fff')
          commit('TOGGLE_MULTI_TAB', false)

          // If the user identity is a student
          if (user.student_profile) {
            commit('SET_IS_TEACHER', false)
            // Set the layout for students
            // save the default UI settings dedicated for student
            commit('TOGGLE_LAYOUT_MODE', 'topmenu')
            commit('TOGGLE_FIXED_HEADER', true)
            commit('TOGGLE_FIXED_SIDERBAR', false)
          } else {
            // if the user identity is a teacher
            commit('SET_IS_TEACHER', true)
            commit('TOGGLE_LAYOUT_MODE', 'sidemenu')
            commit('TOGGLE_FIXED_HEADER', true)
            commit('TOGGLE_FIXED_SIDERBAR', true)
          }

          resolve()
        })
      })
    },

    // 登出
    Logout ({ commit, state }) {
      return new Promise((resolve) => {
        logout().then(() => {
          resolve()
        }).catch(() => {
          resolve()
        }).finally(() => {
          // reset all fields to default
          commit('SET_TOKEN', '')
          Vue.ls.remove(ACCESS_TOKEN)
          commit('SET_SELECTED_COURSE', null)
          commit('SET_EDIT_COURSE_MODE', 3)
        })
      })
    }
  }
}

export default user
