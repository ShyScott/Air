import { axios } from '@/utils/request'

export function getStudentCourses () {
  return axios({
    url: '/courses/',
    method: 'get'
  })
}
