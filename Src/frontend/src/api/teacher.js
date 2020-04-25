import { axios } from '@/utils/request'

export function getTeacherCourses () {
  return axios({
    url: '/courses',
    method: 'get'
  })
}
