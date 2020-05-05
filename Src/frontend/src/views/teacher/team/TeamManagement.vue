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
          <a-icon type="team"/>
          <span>Team Management</span>
        </a-breadcrumb-item>
      </a-breadcrumb>
      <!--Table Area-->
      <div style="margin-top: 25px">
        <a-table :dataSource="this.courseList" :columns="this.teamInfoTableColumns" rowKey="id" :pagination="this.teaminfolistPagination">
          <template slot="operation" slot-scope="text, record">
            <!--tooltip for operation button-->
            <a-tooltip placement="top">
              <template slot="title">
                <span>Click to do team formation settings</span>
              </template>
              <a href="#" @click="showFormOptionsModal(record)"><a-icon type="setting" />Form options</a>
            </a-tooltip>
            <a-popconfirm title="Are you sure to confirm the team formation of this course? If confirmed, no more changes would be allowed." @confirm="confirmTeamFormation(record)" @cancel="cancelTeamFormation">
              <!--tooltip for operation button-->
              <a-tooltip>
                <template slot="title">
                  <span>Click to confirm the team formation of this course</span>
                </template>
                <a class="a-adjust" href="#"><a-icon type="save" />Confirm Teams</a>
              </a-tooltip>
            </a-popconfirm>
          </template>
        </a-table>
      </div>
    </a-card>
  </div>
</template>

<script>
  import { getTeacherCourses, getTeamsList } from '../../../api/teacher'
  export default {
    name: 'TeamManagement',
    data () {
      return {
        // variable used to store all the courses
        courseList: [],
        // variable used to store all the teams info
        teamList: [],
        // Columns for the team list table
        teamInfoTableColumns: [
          {
            title: 'Course Name',
            dataIndex: 'title',
            width: '25%',
            scopedSlots: { customRender: 'title' }
          },
          {
            title: 'Number of Participants',
            dataIndex: 'students_count',
            width: '20%',
            scopedSlots: { customRender: 'students_count' }
          },
          {
            title: 'Participant already in team',
            dataIndex: 'formed_students_count',
            width: '20%',
            scopedSlots: { customRender: 'formed_students_count' }
          },
          {
            title: 'Operation',
            dataIndex: 'operation',
            width: '30%',
            scopedSlots: { customRender: 'operation' }
          }
        ],
        // pagination settings for team info table
        // pagination settings for submission list table
        teaminfolistPagination: {
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
            this.getCourses()
          },
          onChange: (page, pageSize) => {
            this.pageSizeForTeam = pageSize
            this.pageNumForTeam = page
            // re-render
            this.getCourses()
          }
        },
        // page num for team table
        pageNumForTeam: 1,
        // page size for team table
        pageSizeForTeam: 5
      }
    },
    methods: {
      // function used to move to main page
      moveToIndex () {
        this.$router.push('mainpage')
      },
      // function used to get all the courses
      getCourses () {
        getTeacherCourses(this.pageNumForTeam, this.pageSizeForTeam).then(({ data: response }) => {
          this.courseList = response.results
          this.teaminfolistPagination.total = response.count
          // console.log(this.courseList)
        }).catch(error => {
          console.info(error)
          this.$notification.error({
            message: 'Error',
            description: 'Failed to get the information of available courses'
          })
        })
      },
      // function used to get all the teams' info
      // TODO
      getTeams () {
        getTeamsList().then(({ data: response }) => {
          // console.log(response)
        })
      },
      // function executed when user click confirm teams button
      // TODO
      confirmTeamFormation (course) {
        console.log(course)
      },
      // function executed when user click cancel button of teams confirmation
      cancelTeamFormation () {
        // give the feedback
        return this.$notification.info({
          message: 'Info',
          description: 'You have canceled the confirmation of current team formation'
        })
      },
      // function executed when user click the form options button
      showFormOptionsModal (course) {
        console.log(course)
      }
    },
    created () {
      this.getCourses()
      this.getTeams()
    }
  }
</script>

<style scoped>
  .a-adjust {
    color: red;
    margin-left: 20px;
  }
</style>
