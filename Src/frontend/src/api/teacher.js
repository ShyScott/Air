import { axios } from '@/utils/request'
// get all the courses instructed by teacher logging in
export function getTeacherCourses (page, pagesize) {
  return axios({
    url: '/courses/',
    method: 'get',
    params: { page: page, size: pagesize }
  })
}
// get the course information according to id given
export function getCourseInfoById (courseId) {
  return axios({
    url: `/courses/${courseId}/`,
    method: 'get'
  })
}
// get all the students of a course
export function getStudentListOfTheCourse (courseId, page, pagesize) {
  return axios({
    url: '/users/',
    method: 'get',
    params: { course: courseId, page: page, size: pagesize }
  })
}
