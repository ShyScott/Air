import Vue from 'vue'
import axios from 'axios'
import cookie from 'cookie'
import store from '@/store'
import notification from 'ant-design-vue/es/notification'
import { VueAxios } from './axios'
import { ACCESS_TOKEN } from '@/store/mutation-types'

// 创建 axios 实例
const service = axios.create({
  baseURL: '/api',
  timeout: 6000, // 请求超时时间,
  withCredentials: true
})

const err = (error) => {
  if (error.response) {
    const data = error.response.data
    const token = Vue.ls.get(ACCESS_TOKEN)
    if (error.response.status === 403) {
      notification.error({
        message: 'Forbidden',
        description: data.message
      })
    }
    if (error.response.status === 401 && error.response.config.url.indexOf('/users/me/') === -1) {
      notification.error({
        message: 'Unauthorized',
        description: 'Your login state is invalid. Please re-login.'
      })
      if (token) {
        store.dispatch('Logout').then(() => {
          setTimeout(() => {
            window.location.reload()
          }, 1500)
        })
      }
    }
  }
  return Promise.reject(error)
}

// request interceptor
service.interceptors.request.use(config => {
  // const token = Vue.ls.get(ACCESS_TOKEN)
  // if (token) {
  //   config.headers['Authorization'] = token // 让每个请求携带自定义 token 请根据实际情况自行修改
  // }
  const token = cookie.parse(document.cookie).csrftoken
  if (token) {
    config.headers['X-CSRFToken'] = token
  }
  return config
}, err)

// response interceptor
service.interceptors.response.use((response) => {
  return {
    status: response.status,
    data: response.data
  }
}, err)

const installer = {
  vm: {},
  install (Vue) {
    Vue.use(VueAxios, service)
  }
}

export {
  installer as VueAxios,
  service as axios
}
