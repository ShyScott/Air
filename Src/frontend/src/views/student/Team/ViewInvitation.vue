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
          placeholder="Please select the course"
          style="width: 400px"
          show-search
          :filterOption="false"
          @search="handleSearch"
          @change="handleChange"
        >
          <a-icon slot="suffixIcon" type="smile" />
        </a-select>
      </div>
      <!--Table area for the invitation list-->
      <a-table :dataSource="this.invitationList" rowKey="id" :columns="invitationListColumns"></a-table>
    </a-card>
  </div>
</template>

<script>
  import { getCoursesByQuery, getInvitation } from '../../../api/student'
  import { mapGetters } from 'vuex'

  export default {
    name: 'ViewInvitation',
    data () {
      return {
        // variable used to store all the courses
        courseList: [],
        // variable used to store the invitations
        invitationList: [],
        // columns settings for invitation list
        invitationListColumns: [
          {
            title: 'Course Name',
            dataIndex: 'course.title',
            width: '20%'
          }
        ]
      }
    },
    methods: {
      // function used to move to main page
      moveToIndex () {
        this.$router.push({ name: 'Index' })
      },
      // function used to move to the team management page
      moveToTeamManagementPage () {
        this.$router.push('/team')
      },
      // TODO: function used to search the target course
      handleSearch (value) {
        const parameter = { title: value }
        getCoursesByQuery(parameter).then(({ data: response }) => {
          this.courseList = response.results
          // console.log(this.courseList)
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
      handleChange () {
      },
      // function used to get all the invitations of current student
      getAllInvitations () {
        getInvitation().then(({ data: response }) => {
          this.invitationList = response.results
          console.log(this.invitationList)
        })
      }
    },
    created () {
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
