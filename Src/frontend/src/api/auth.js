import { axios } from '@/utils/request'

export function login (data) {
  return axios({
    url: '/token/',
    method: 'post',
    data
  })
}

export function getMyInfo () {
  return axios({
    url: '/users/me/',
    method: 'get'
  })
}
