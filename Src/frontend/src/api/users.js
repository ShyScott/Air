import { axios } from '@/utils/request'
import store from '@/store'

export function changePassword (data) {
  return axios({
    url: '/users/change_password/',
    method: 'put',
    data
  })
}

export function changeAvatar (formData) {
  return axios({
    url: `/users/${store.getters.userId}/avatar/`,
    method: 'put',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data: formData
  })
}
