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
// function used to vote the team leader
export function voteTeamLeader (teamId, parameter) {
  return axios({
    url: `/teams/${teamId}/vote_leader/`,
    method: 'patch',
    data: parameter
  })
}
// function used to quit the team
export function exitTeam (teamId) {
  return axios({
    url: `/teams/${teamId}/quit/`,
    method: 'get'
  })
}
// function used to query student by id or name
export function queryStudent (parameter) {
  return axios({
    url: '/users/',
    method: 'get',
    params: parameter
  })
}
// function executed to send invitation to target person
export function inviteSomeone (parameter) {
  return axios({
    url: '/invitations/',
    method: 'post',
    data: parameter
  })
}
// get courses by query
export function getCoursesByQuery (query) {
  return axios({
    url: '/courses/',
    method: 'get',
    params: query
  })
}
export function getInvitation (parameter) {
  return axios({
    url: '/invitations/',
    method: 'get',
    params: parameter
  })
}
