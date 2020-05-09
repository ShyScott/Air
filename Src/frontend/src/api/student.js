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
// get invitee's invitations
export function getInvitation (parameter) {
  return axios({
    url: '/invitations/',
    method: 'get',
    params: parameter
  })
}
// get invitations info by course id
export function getInvitationsByCourseId (parameter) {
  return axios({
    url: `/invitations/`,
    method: 'get',
    params: parameter
  })
}
// function used to respond to the invitation request
export function respondToRequest (invitationId, parameter) {
  return axios({
    url: `/invitations/${invitationId}/respond/`,
    method: 'put',
    data: parameter
  })
}
// function used to get the submissions of one course
export function getSubmissionList (parameter) {
  return axios({
    url: '/submissions/',
    method: 'get',
    params: parameter
  })
}
// function use course id to get course info
export function getCourseInfoById (courseId) {
  return axios({
    url: `/courses/${courseId}/`,
    method: 'get'
  })
}
// function used to submit the results of submission assessment
export function submitAssessmentResults (parameter) {
  return axios({
    url: '/contributions/',
    method: 'post',
    data: parameter
  })
}
// function used to submit the assessment towards leader
export function submitLeaderAssessment (teamId, parameter) {
  return axios({
    url: `/teams/${teamId}/assess_leader/`,
    method: 'put',
    data: parameter
  })
}
