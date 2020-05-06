import { axios } from '@/utils/request'

// function used for student to get the course info
export function getStudentCourses (parameter) {
  return axios({
    url: '/courses/',
    method: 'get',
    params: parameter
  })
}
// function used for student to create a new team
export function createNewTeam (parameter) {
  return axios({
    url: '/teams/form_new/',
    method: 'post',
    data: parameter
  })
}
// function used to query by team name
export function queryCourse (parameter) {
  return axios({
    url: '/courses/',
    method: 'get',
    params: parameter
  })
}
