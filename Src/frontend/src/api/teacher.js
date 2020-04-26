import { axios } from '@/utils/request'
// get all the courses instructed by teacher logging in
export function getTeacherCourses () {
  return axios({
    url: '/courses',
    method: 'get'
  })
}
// get the course information according to id given
export function getCourseInfoById (parameter) {
  return axios({
    url: '/courses/' + parameter,
    method: 'get'
  })
}
// get all the students of a course
export function getStudentListOfTheCourse (courseId) {
  return axios({
    url: '/users/?course=' + courseId,
    method: 'get'
  })
}
