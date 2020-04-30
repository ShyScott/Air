<template>
  <div>
    <!--root template-->
    <template>
      <a-card>
        <!--breadcrumb area-->
        <a-breadcrumb>
          <a-breadcrumb-item href="">
            <a-icon @click="moveToIndex" type="home"/>
            <span @click="moveToIndex">Main</span>
          </a-breadcrumb-item>
          <a-breadcrumb-item href="">
            <a-icon type="upload"/>
            <span>Submission Management</span>
          </a-breadcrumb-item>
        </a-breadcrumb>
        <!--Select Area-->
        <div style="margin-top: 20px">
          <span style="margin-right: 15px">Target Course: </span>
          <a-select placeholder="Please select the course" style="width: 250px" @change="handleChange">
            <a-icon slot="suffixIcon" type="smile" />
            <a-select-option v-for="(item, i) in this.courseList" :key="i" :value="item.id">
              {{ item.title }}
            </a-select-option>
          </a-select>
        </div>
        <!--New submission Button-->
        <div style="margin-top: 20px">
          <a-button type="primary" icon="cloud-upload" size="default" style="width: 180px"> New Submission </a-button>
        </div>
        <!--Alert Area-->
        <a-alert style="margin-top: 20px; margin-bottom: 20px" message="Reminder: Please select the course before further management operations" type="info" showIcon />
        <!--Table Area-->
        <a-table :dataSource="this.submissionList" rowKey="id" :columns="this.submissionListColumns">
          <template slot="operation" slot-scope="text, record">
            <!--tooltip for operation button-->
            <a-tooltip placement="top">
              <template slot="title">
                <span>Click to edit this submission</span>
              </template>
              <a href="#" @click="editSubmission(record)"><a-icon type="edit" />Edit</a>
            </a-tooltip>
            <a-popconfirm title="Are you sure to delete this submission?" @confirm="confirmDeleteSubmission(record)" @cancel="cancelDeleteSubmission">
              <!--tooltip for operation button-->
              <a-tooltip>
                <template slot="title">
                  <span>Click to delete this course</span>
                </template>
                <a class="a-adjust" href="#"><a-icon type="delete" />Delete</a>
              </a-tooltip>
            </a-popconfirm>
          </template>
        </a-table>
      </a-card>
    </template>
  </div>
</template>

<script>
  import { getTeacherCourses, getSubmissionList } from '../../../api/teacher'
  export default {
    name: 'SubmissionManagement',
    data () {
      return {
        // list used store all the course info of current teacher
        courseList: [],
        // variable used to indicate the current selected course
        selectedCourseId: '',
        // list used to store the submission of course selected
        submissionList: [],
        // columns for the submission list table
        submissionListColumns: [{
        // Submission ID column
        title: ' Submission ID ',
        dataIndex: 'id',
        width: '25%',
        scopedSlots: { customRender: 'id' }
      },
        {
          // Submission Title column
          title: 'Submission Title',
          dataIndex: 'title',
          width: '25%',
          scopedSlots: { customRender: 'title' }
        },
        {
          // Percentage column
          title: 'Percentage (%)',
          dataIndex: 'percentage',
          width: '25%',
          scopedSlots: { customRender: 'percentage' }
        },
        {
          // operation column
          title: 'Operation',
          dataIndex: 'operation',
          width: '25%',
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
      // function used to get all the course info of current teacher
      getCourses () {
        getTeacherCourses().then(({ data: response }) => {
          this.courseList = response.results
          // console.log(this.courseList)
        })
      },
      // function used to get the submission list of the current course
      getSubmissions (courseId) {
        getSubmissionList(courseId).then(({ data: response }) => {
          this.submissionList = response.results
          console.log(this.submissionList)
        })
      },
      // function executed when user select the target course
      handleChange (value) {
        this.selectedCourseId = value
        // console.log(this.selectedCourseId)
        this.getSubmissions(this.selectedCourseId)
      },
      // function executed when user click the edit button
      editSubmission (course) {
        console.log(course.id)
      },
      // function executed when user confirm to delete the submission
      confirmDeleteSubmission (course) {
        console.log(course.id)
      },
      // function executed when user cancel the submission delete
      cancelDeleteSubmission () {
        console.log('cancel')
      }
    },
    created () {
      // get all the course info before page rendering
      this.getCourses()
    }
  }
</script>

<style scoped>
  .a-adjust {
    color: red;
    margin-left: 10px;
  }
</style>
