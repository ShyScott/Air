<template>
  <div>
    <!--Make sure that user cannot access this page by inputing url after confirmation is done-->
    <div v-if="this.hide === false">
      <a-spin size="large" :spinning="this.spinning">
        <a-card>
          <!--breadcrumb area-->
          <a-breadcrumb>
            <a-breadcrumb-item href="">
              <a-icon @click="moveToIndex" type="home"/>
              <span @click="moveToIndex">Main</span>
            </a-breadcrumb-item>
            <a-breadcrumb-item href="">
              <a-icon @click="moveBackToTeamManagement" type="team"/>
              <span @click="moveBackToTeamManagement">Team Management</span>
            </a-breadcrumb-item>
            <a-breadcrumb-item href="">
              <a-icon type="lock"/>
              <span>Formation Confirmation</span>
            </a-breadcrumb-item>
          </a-breadcrumb>
          <div style="margin-top: 20px; color: darkgray">
            Current Form Method: <span style="color: #1A8FFF">{{ this.formMethod }}</span>
          </div>
          <!--Team list table area-->
          <a-table
            style="margin-top: 15px"
            :dataSource="teamList"
            :columns="teamListColumns"
            rowKey="name"
            :pagination="teamListPagination"
          >
            <template slot="teamMember" slot-scope="text, record">
              <span style="margin-right: 20px" v-for="item in record.members" :key="item.id">
                {{ item.username }}
              </span>
            </template>
          </a-table>
          <!--Alert area-->
          <a-alert
            style="margin-top: 50px"
            message="Reminder: Students with no team yet are shown below. (For method 1 4 5, all students should be in team before confirmation)"
            type="info"
            show-icon
          />
          <!--Table for students still not in any team-->
          <a-table style="margin-top: 15px" :dataSource="studentWithNoTeamList" :columns="studentlistColumns" :pagination="studentListPagination" rowKey="id"></a-table>
          <!--Button area-->
          <div style="display: flex; justify-content: flex-end; flex-direction: row; margin-top: 30px; margin-right: 30px">
            <span style="margin-right: 25px">
              <a-button type="danger" @click="cancelConfirmation"><a-icon type="disconnect" /> Cancel </a-button>
            </span>
            <span style="margin-right: 25px">
              <a-button type="default" :disabled="formMethod === 1" @click="regenerateTeams"><a-icon type="reload" /> Regenerate </a-button>
            </span>
            <span>
              <a-button :disabled="((studentWithNoTeamList.length !== 0 && (this.formMethod === 1 || this.formMethod === 4 || this.formMethod === 5)) || (this.formMethod === null))" type="primary" @click="submitTeamConfirmation"><a-icon type="lock" /> Confirm </a-button>
            </span>
          </div>
        </a-card>
      </a-spin>
    </div>
    <div v-else>
      <template>
        <a-result status="404" title="404" sub-title="Sorry, the page you visited does not exist.">
          <template #extra>
            <a-button @click="$router.push({ name: 'Index' })" type="primary">
              Back Home
            </a-button>
          </template>
        </a-result>
      </template>
    </div>
  </div>
</template>

<script>
  import {
    confirmTeamFormation,
    generateTeam,
    getCourseInfoById,
    getNoTeamStudent
  } from '../../../api/teacher'

  export default {
    name: 'FormConfirmation',
    data () {
      return {
        // control the display of form confirmation page
        hide: false,
        // spinning control
        spinning: false,
        // variable used to store the team list
        teamList: [],
        // parameter transferred from the team management page
        selectedCourseId: '',
        // list used to store those students still not in any time
        studentWithNoTeamList: [],
        // pagination for the table list
        pageSizeForTeam: 5,
        pageNumForTeam: 1,
        // columns used for team list table
        teamListColumns: [
          {
            title: 'Team Name',
            dataIndex: 'name',
            width: '40%',
            align: 'center',
            scopedSlots: { customRender: 'teamName' }
          },
          {
            title: 'Team member',
            dataIndex: 'members',
            width: '60%',
            align: 'center',
            scopedSlots: { customRender: 'teamMember' }
          }
        ],
        // columns used for student with no team list table
        studentlistColumns: [
          {
            title: 'Student Name',
            dataIndex: 'username',
            width: '33.3%',
            align: 'center',
            scopedSlots: { customRender: 'username' }
          },
          {
            title: 'Student ID',
            dataIndex: 'student_profile.student_id',
            width: '33.3%',
            align: 'center',
            scopedSlots: { customRender: 'studentId' }
          },
          {
            title: 'GPA',
            dataIndex: 'student_profile.gpa',
            width: '33.3%',
            align: 'center',
            scopedSlots: { customRender: 'gpa' }
          }
        ],
        // pagination settings for team list table
        teamListPagination: {
          // default page size
          defaultPageSize: 5,
          // Show the number of total items
          showTotal: (total) => `Total ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '15', '20', '25'],
          onShowSizeChange: (current, pageSize) => {
            this.pageNumForTeam = current
            this.pageSizeForTeam = pageSize
            // re-render
          },
          onChange: (page, pageSize) => {
            this.pageSizeForTeam = pageSize
            this.pageNumForTeam = page
            // re-render
          }
        },
        // pagination settings for student list table
        studentListPagination: {
          // default page size
          defaultPageSize: 5,
          // Show the number of total items
          showTotal: (total) => `Total ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '15', '20', '25'],
          onShowSizeChange: (current, pageSize) => {
            this.pageNumForStudent = current
            this.pageSizeForStudent = pageSize
            // re-render
            this.getStudentsWithoutTeam()
          },
          onChange: (page, pageSize) => {
            this.pageSizeForStudent = pageSize
            this.pageNumForStudent = page
            // re-render
            this.getStudentsWithoutTeam()
          }
        },
        pageNumForStudent: 1,
        pageSizeForStudent: 5,
        // form method of current course
        formMethod: 0,
        // total info of current course
        currentCourseInfo: {}
      }
    },
    methods: {
      // function used to get the team list of current course
      getGeneratedTeams () {
        this.teamList = []
        generateTeam(this.selectedCourseId).then(({ data: response }) => {
          // console.log(response)
          this.teamList = response
        }).catch(error => {
          // if error occurs
          if (error.response) {
            console.info(error.response)
            if (error.response.data) {
              const errorInfo = error.response.data[0]
              return this.$notification.warning({
                message: 'Warning',
                description: errorInfo
              })
            }
            return this.$notification.error({
              message: 'Error',
              description: 'Failed to get the team info'
            })
          }
        })
      },
      // function used to move to main page
      moveToIndex () {
        this.$router.push({ name: 'Index' })
      },
      // function used to move back to team management page
      moveBackToTeamManagement () {
        this.$router.push({ name: 'TeamManagement' })
      },
      // function used to get student list of those who still do not have a team
      getStudentsWithoutTeam () {
        const courseId = this.selectedCourseId
        getNoTeamStudent(courseId).then(({ data: response }) => {
          // console.log(response)
          this.studentWithNoTeamList = response
        }).catch(error => {
          // if error occurs
          if (error.response) {
            // give the warning
            return this.$notification.error({
              message: 'Error',
              description: 'Failed to get the information of students without teams'
            })
          }
        })
      },
      // function used to be back to the team management page
      cancelConfirmation () {
        this.$router.push({ name: 'TeamManagement' })
      },
      // function executed when user click the regenerate button
      regenerateTeams () {
        this.getGeneratedTeams()
      },
      // function used to get the course's form method
      getFormMethod () {
        getCourseInfoById(this.selectedCourseId).then(({ data: response }) => {
          // console.log(response)
          this.formMethod = response.form_method
          // console.log(this.formMethod)
        }).catch(error => {
          if (error.response) {
            console.info(error.response)
            return this.$notification.error({
              message: 'Error',
              description: 'Failed to get the course information'
            })
          }
        })
      },
      // function used for teacher to confirm the team formation
      submitTeamConfirmation () {
        // console.log(this.teamList)
        const parameter = []
        // process the data
        for (let i = 0; i < this.teamList.length; i++) {
          // push all the member in each team to the parameter's members
          parameter.push({
            name: this.teamList[i].name,
            course: this.selectedCourseId,
            members: this.teamList[i].members.map((item) => item.id)
          })
        }
        confirmTeamFormation(this.selectedCourseId, parameter).then(({ data: response }) => {
          this.$notification.success({
            message: 'Success',
            description: 'Confirm the team formation successful'
          })
          this.spinning = true
          setTimeout(() => { this.$router.push({ name: 'TeamManagement' }) }, 2000)
        }).catch(error => {
          if (error.response) {
            console.info(error.response)
            var errorInfo = 'Failed to confirm the team formation'
            if (error.response.data) errorInfo = error.response.data[0]
            this.$notification.error({
              message: 'Error',
              description: errorInfo
            })
          }
        })
      },
      // get current course's info
      getCourseInfo () {
        getCourseInfoById(this.selectedCourseId).then(({ data: response }) => {
          this.currentCourseInfo = response
          if (this.currentCourseInfo.is_confirmed === true) {
            this.hide = true
          }
          // console.log(this.currentCourseInfo)
        })
      }
    },
    created () {
      // store the target course id
      const courseId = this.$route.params.courseId
      this.selectedCourseId = courseId
      // get the info of current course
      this.getCourseInfo()
      // get all the teams of current course
      this.getGeneratedTeams()
      // get students without team yet
      this.getStudentsWithoutTeam()
      // get the form method of current course
      this.getFormMethod()
    }
  }
</script>

<style scoped>

</style>
