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
            <span v-if="record.team_in.leader === userId">
              <a-icon style="color: #1A8FFF" type="solution"></a-icon>
              <a href="#" @click="moveToAssessSubmissionPage(record.id)"> Assess submissions </a>
            </span>
            <span v-else>
              <a-icon style="color: #1A8FFF" type="rocket"></a-icon>
              <a href="#" @click="showAssessLeaderModal(record)"> Assess team leader </a>
            </span>
          </template>
        </a-table>
      </div>
    </a-card>
    <!--Assess leader modal-->
    <a-modal width="800px" v-model="assessLeaderModalVisible" title="Assess Team Leader" on-ok="handleOk">
      <template slot="footer">
        <a-button key="back" @click="handleCancel">
          Cancel
        </a-button>
        <a-button key="submit" type="primary" @click="handleOk">
          Submit
        </a-button>
      </template>
      <a-form-model
        v-model="assessLeaderForm"
        ref="assessLeaderRef"
        :label-col="labelCol"
        :wrapper-col="wrapperCol"
      >
        <a-form-model-item label="Submission Title">
          <a-input :disabled="true" v-model="assessLeaderForm.courseTitle"></a-input>
        </a-form-model-item>
        <template v-if="selectedCourse !== null">
          <a-form-model-item>
            <span v-for="(item, i) in selectedCourse.team_in.members" :key="i">
              <span style="margin-left: 36px; margin-right: 20px" v-if="item.id === selectedCourse.team_in.leader">
                Rate for leader {{ item.username }} :
              </span>
            </span>
            <a-rate v-model="assessLeaderForm.rateForLeader" :tooltips="desc" :allow-clear="false">
              <a-icon slot="character" type="smile" />
            </a-rate>
          </a-form-model-item>
        </template>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { getStudentCourses, submitLeaderAssessment } from '../../../api/student'
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
          showTotal: (total) => `Total ${ total } items`,
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
        ],
        // variable used to control the display of assess leader modal
        assessLeaderModalVisible: false,
        // form object for assess team leader modal
        assessLeaderForm: {
          courseTitle: '',
          rateForLeader: 5
        },
        // layout settings for the add submission form
        labelCol: { span: 5 },
        wrapperCol: { span: 16 },
        // course selected in the course list
        selectedCourse: null,
        // description for the leader rate level
        desc: ['VERY BAD', 'BAD', 'FAIR', 'GOOD', 'VERY GOOD']
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
          // console.log(this.courseList)
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
      },
      // function used to show assess leader modal
      showAssessLeaderModal (course) {
        this.selectedCourse = course
        this.assessLeaderForm.courseTitle = course.title
        this.assessLeaderModalVisible = true
      },
      // function executed when user press the cancel button in assess leader modal
      handleCancel () {
        // reset and hide the modal
        this.assessLeaderForm.rateForLeader = 5
        this.assessLeaderModalVisible = false
      },
      // function executed when user press the submit button in assess leader modal
      handleOk () {
        this.assessLeader()
        // reset and hide the modal
        this.assessLeaderForm.rateForLeader = 5
        this.assessLeaderModalVisible = false
      },
      // submit the leader assessment
      assessLeader () {
        // process data
        const level = this.assessLeaderForm.rateForLeader - 3
        const parameter = { bonus: level }
        submitLeaderAssessment(this.selectedCourse.team_in.id, parameter).then(() => {
          this.$notification.success({
            message: 'Success',
            description: 'Submit the leader assessment successfully'
          })
        }).catch(error => {
          console.info(error.response)
          this.$notification.error({
            message: 'Error',
            description: 'Failed to submit the assessment to leader'
          })
        })
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
