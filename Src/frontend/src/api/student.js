import { axios } from '@/utils/request'

export function getStudentCourses (parameter) {
  return axios({
    url: '/courses/',
    method: 'get',
    params: parameter
  })
}
