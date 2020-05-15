import { axios } from '@/utils/request'

export function changePassword (data) {
  return axios({
    url: '/users/change_password/',
    method: 'put',
    data
  })
}
