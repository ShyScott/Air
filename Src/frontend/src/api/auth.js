import { axios } from '@/utils/request'
import qs from 'qs'

export function login (data) {
  return axios({
    baseURL: '/api-auth',
    url: '/login/',
    method: 'post',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    params: { next: '/api/users/me/' },
    data: qs.stringify(data)
  })
}

export function logout () {
  return axios({
    baseURL: '/api-auth',
    url: '/logout/',
    method: 'get',
    params: { next: '/api-auth/login/' }
  })
}

export function getMyInfo () {
  return axios({
    url: '/users/me/',
    method: 'get'
  })
}
