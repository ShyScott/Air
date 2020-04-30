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

// get the student info according to the query info
export function getStudentByQuery (queryName, courseId) {
  return axios({
    url: '/users/',
    method: 'get',
    params: { username: queryName, course: courseId }
  })
}

// delete the course selected by teacher
export function deleteCourse (courseId) {
  return axios({
    url: `/courses/${courseId}`,
    method: 'delete'
  })
}
// remove the student from the given course
export function removeStudent (courseId, studentId) {
  return axios({
    url: `/courses/${courseId}/remove_student/`,
    method: 'post',
    data: { user: studentId }
  })
}
// add a student to a selected course
export function addStudentToTheCourse (parameter) {
  return axios({
    url: `/users/`,
    method: 'post',
    data: parameter
  })
}
// get the submission list of current course
export function getSubmissionList (courseId) {
  return axios({
    url: `submissions`,
    method: 'get',
    params: { course: courseId }
  })
}
