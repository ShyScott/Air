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
          <a-icon type="like"/>
          <span>Assessment Management</span>
        </a-breadcrumb-item>
      </a-breadcrumb>
      <!--search bar-->
      <a-row style="margin-top: 30px">
        <a-col :span="7">
          <a-input-search placeholder="Please input course name" v-model="queryContent" enter-button @search="onSearch" />
        </a-col>
      </a-row>
      <!--Table area-->
      <div style="margin-top: 30px">
        <!--team role area-->
        <a-table :dataSource="courseList" :pagination="paginationForCourseTable" rowKey="id" :columns="courseListColumns">
          <template slot="role" slot-scope="text, record">
            <span v-if="record.team_in.leader === userId">
              Leader <a-icon style="color: goldenrod" type="crown"></a-icon>
            </span>
            <span v-else>
              Member <a-icon style="color: #1A8FFF" type="user"></a-icon>
            </span>
          </template>
          <!--operation area-->
          <template slot="operation" slot-scope="text, record">
            <span style="margin-right: 15px" v-if="record.team_in.leader === userId">
              <a-icon style="color: #1A8FFF" type="solution"></a-icon>
              <a href="#" @click="moveToAssessSubmissionPage(record.id)"> Assess submissions </a>
            </span>
            <span>
              <a-icon style="color: #1A8FFF" type="rocket"></a-icon>
              <a href="#"> Assess team leader </a>
            </span>
          </template>
        </a-table>
      </div>
    </a-card>
  </div>
</template>

<script>
  import { getStudentCourses } from '../../../api/student'
  import { mapGetters } from 'vuex'

  export default {
    name: 'AssessmentManagement',
    data () {
      return {
        // variable used to store all the couses' info
        courseList: [],
        // object used to adjust the pagination of the course table
        paginationForCourseTable: {
          current: 1,
          pageSize: 5,
          // Show the number of total items
          showTotal: (total) => `Totally ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '12', '15', '25'],
          onShowSizeChange: (current, pageSize) => {
            this.paginationForCourseTable.current = current
            this.paginationForCourseTable.pageSize = pageSize
            this.getCourses()
          },
          onChange: (current, pageSize) => {
            this.paginationForCourseTable.pageSize = pageSize
            this.paginationForCourseTable.current = current
            this.getCourses()
          }
        },
        // what student search
        queryContent: '',
        // columns settings for the course list table
        courseListColumns: [
          {
            // course name column
            title: 'Course Name',
            dataIndex: 'title',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'courseName' }
          },
          {
            // team name column
            title: 'Team Name',
            dataIndex: 'team_in.name',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'teamName' }
          },
          {
            // team role column
            title: 'Role',
            dataIndex: 'team_in',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'role' }
          },
          {
            // operation column
            title: 'Operation',
            dataIndex: 'operation',
            width: '40%',
            align: 'center',
            scopedSlots: { customRender: 'operation' }
          }
        ]
      }
    },
    methods: {
      // function used to move to main page
      moveToIndex () {
        this.$router.push('mainpage')
      },
      // function used to get the course info of current student
      getCourses (isSearch = false) {
        // reset the page num for the table
        if (isSearch) this.paginationForCourseTable.current = 1
        const parameter = {
          page: this.paginationForCourseTable.current,
          size: this.paginationForCourseTable.pageSize
        }
        // if user wants to search
        if (this.queryContent !== '') parameter.title = this.queryContent
        getStudentCourses(parameter).then(({ data: response }) => {
          this.courseList = response.results
          // filter the course with no team yet
          this.courseList = this.courseList.filter((item) => {
            return item.team_in !== null && item.team_in.leader !== null
          })
          this.paginationForCourseTable.total = this.courseList.length
          console.log(this.courseList)
        }).catch(error => {
          if (error.response) {
            console.info(error.response)
            return this.$notification.error({
              message: 'Error',
              description: 'Failed to get the information of available courses'
            })
          }
        })
      },
      // executed when search button is pressed
      onSearch () {
        this.getCourses(true)
      },
      // function used to move the assess submission page
      moveToAssessSubmissionPage (courseId) {
        this.$router.push({ name: 'AssessSubmission', params: { courseId: courseId } })
      }
    },
    created () {
      this.getCourses()
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
