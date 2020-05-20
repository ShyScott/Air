<template>
  <div>
    <a-card>
      <!--breadcrumb area-->
      <a-breadcrumb>
        <a-breadcrumb-item href="">
          <a-icon @click="moveToIndex" type="home"/>
          <span @click="moveToIndex">Main</span>
        </a-breadcrumb-item>
        <a-breadcrumb-item href="">
          <a-icon @click="moveToTeamManagementPage" type="team"/>
          <span @click="moveToTeamManagementPage">Team Management</span>
        </a-breadcrumb-item>
        <a-breadcrumb-item href="">
          <a-icon type="star"/>
          <span>View Invitation</span>
        </a-breadcrumb-item>
      </a-breadcrumb>
      <!--Select Area-->
      <div style="margin-top: 40px">
        <span style="margin-right: 15px"> Course Name: </span>
        <a-select
          placeholder="Select a course. Input course name to filter."
          style="width: 400px"
          show-search
          :filterOption="false"
          @search="handleSearch"
          @change="handleChange"
        >
          <a-icon slot="suffixIcon" type="smile" />
          <a-select-option value="0">
            All
          </a-select-option>
          <a-select-option v-for="(item, i) in this.courseList" :value="item.id" :key="i">
            {{ item.title }}
          </a-select-option>
        </a-select>
      </div>
      <!--Table area for the invitation list-->
      <a-table style="margin-top: 30px" :dataSource="invitationList" rowKey="id" :columns="invitationListColumns" :pagination="invitationListPagination">
        <!--Team member area-->
        <template slot="teamMember" slot-scope="text, record">
          <span v-for="(item, i) in record.team.members" :key="i">
            {{ item.username }}
          </span>
        </template>
        <!--Operation area-->
        <template slot="operation" slot-scope="text, record">
          <a @click="acceptInvitation(record)"><a-icon type="check" /> Accept </a>
          <a style="color: red; margin-left: 20px" @click="rejectInvitation(record)"><a-icon type="stop" /> Reject </a>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script>
  import { getCoursesByQuery, getInvitation, respondToRequest } from '@/api/student'
  import { mapGetters } from 'vuex'
  import { getTeacherCourses } from '@/api/teacher'

  export default {
    name: 'ViewInvitation',
    data () {
      return {
        // variable used to store all the courses
        courseList: [],
        // the course got selected
        selectedCourse: '',
        // variable used to store the invitations
        invitationList: [],
        // columns settings for invitation list
        invitationListColumns: [
          {
            title: 'Course Name',
            dataIndex: 'course.title',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'courseName' }
          },
          {
            title: 'Team Name',
            dataIndex: 'team.name',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'teamName' }
          },
          {
            title: 'Team Members',
            dataIndex: 'team.members',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'teamMember' }
          },
          {
            title: 'Inviter',
            dataIndex: 'inviter.username',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'inviter' }
          },
          {
            title: 'Operation',
            dataIndex: 'operation',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'operation' }
          }
        ],
        // pagination settings for the invitations list
        invitationListPagination: {
          current: 1,
          pageSize: 5,
          // Show the number of total items
          showTotal: (total) => `Total ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '12', '15', '25'],
          onShowSizeChange: (current, pageSize) => {
            this.invitationListPagination.current = current
            this.invitationListPagination.pageSize = pageSize
            if (this.selectedCourseId) this.getAllInvitations(true)
            else this.getAllInvitations()
          },
          onChange: (current, pageSize) => {
            this.invitationListPagination.pageSize = pageSize
            this.invitationListPagination.current = current
            if (this.selectedCourseId) this.getAllInvitations(true)
            else this.getAllInvitations()
          }
        }
      }
    },
    methods: {
      // function used to move to main page
      moveToIndex () {
        this.$router.push({ name: 'Index' })
      },
      // get all courses
      getCourses () {
        getTeacherCourses().then(({ data: response }) => {
          this.courseList = response.results
        }).catch(error => {
          console.info(error)
          this.$notification.error({
            message: 'Error',
            description: 'Failed to get the information of available courses'
          })
        })
      },
      // function used to move to the team management page
      moveToTeamManagementPage () {
        this.$router.push('/team')
      },
      handleSearch (value) {
        const parameter = { title: value }
        getCoursesByQuery(parameter).then(({ data: response }) => {
          this.courseList = response.results
          // console.log(this.courseList)
          this.getAllInvitations(true)
        }).catch(error => {
          if (error.response) {
            this.$notification.error({
              message: 'Error',
              description: 'Failed to search ' + value
            })
          }
        })
      },
      // TODO:function executed when user select the target course
      handleChange (value) {
        this.selectedCourse = value
        // use the course id to get invitations of the course
        this.getAllInvitations(true)
      },
      // function used to get all the invitations of current student
      getAllInvitations (isSearch = false) {
        const parameter = { invitee: true, page: this.invitationListPagination.current, size: this.invitationListPagination.pageSize }
        // reset page num for search
        if (isSearch) this.invitationListPagination.current = 1
        // check if user wants to query all the invitations
        // console.log(this.selectedCourse)
        if (this.selectedCourse !== '0') {
          // if user wants to search
          parameter.course = this.selectedCourse
          // reset
          this.selectedCourse = ''
        } else {
          this.selectedCourse = ''
        }
        getInvitation(parameter).then(({ data: response }) => {
          this.invitationList = response.results
          // console.log(this.invitationList)
          // filter those invitations outdated
          this.invitationList = this.invitationList.filter((item) => {
            return item.status === 0
          })
          this.invitationListPagination.total = this.invitationList.length
          // console.log(this.invitationList)
        }).catch(error => {
          if (error.response) {
            return this.$notification.error({
              message: 'Error',
              description: 'Failed to get the information of invitations'
            })
          }
        })
      },
      // function used to accept the invitation request
      acceptInvitation (invitation) {
        // process data
        // 1 indicate accept
        const parameter = { status: 1 }
        respondToRequest(invitation.id, parameter).then(({ data: response }) => {
          this.$notification.success({
            message: 'Success',
            description: 'Invitation has been accepted'
          })
          // re-render
          this.getAllInvitations()
        }).catch(error => {
          if (error.response) {
            console.info(error.response)
            this.$notification.error({
              message: 'Error',
              description: 'Failed to accept the invitation'
            })
          }
        })
      },
      // function used to reject the invitation request
      rejectInvitation (invitation) {
        // process data
        // 1 indicate accept
        const parameter = { status: -1 }
        respondToRequest(invitation.id, parameter).then(({ data: response }) => {
          this.$notification.success({
            message: 'Success',
            description: 'Invitation has been rejected'
          })
          // re-render
          this.getAllInvitations()
        }).catch(error => {
          if (error.response) {
            console.info(error.response)
            this.$notification.error({
              message: 'Error',
              description: 'Failed to reject the invitation'
            })
          }
        })
      }
    },
    created () {
      this.getCourses()
      this.getAllInvitations()
    },
    computed: {
      ...mapGetters([
        'userId'
      ])
    }
  }
</script>

<style scoped>

</style>
