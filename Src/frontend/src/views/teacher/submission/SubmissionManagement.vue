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
          <a-button type="primary" icon="cloud-upload" size="default" style="width: 180px" @click="showAddSubmissionModal"> New Submission </a-button>
        </div>
        <!--Alert Area-->
        <a-alert style="margin-top: 20px; margin-bottom: 20px" message="Reminder: Please select the course before further management operations" type="info" showIcon />
        <!--Table Area-->
        <a-table :dataSource="this.submissionList" rowKey="id" :columns="this.submissionListColumns" :pagination="this.submissionListPagination">
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
      <a-modal v-model="addSubmissionModalVisible" title="Add a new Submission" width="800px">
        <template slot="footer">
          <a-button key="Cancel" @click="handleAddStudentModalReset">Reset</a-button>
          <a-button key="submit" type="primary" @click="handleAddSubmissionOk">
            Submit
          </a-button>
        </template>
        <div style="width: 640px">
          <a-form-model
            :model="addSubmissionForm"
            :rules="addSubmissionRules"
            ref="addSubmissionForRef"
            :label-col="labelCol"
            :wrapper-col="wrapperCol">
            <!--Course name-->
            <a-form-model-item label="Course name">
              <a-input v-model="addSubmissionForm.coursename" :disabled="true"></a-input>
            </a-form-model-item>
            <!--Submission Title-->
            <a-form-model-item label="Submission Title" prop="title">
              <a-input v-model="addSubmissionForm.title"></a-input>
            </a-form-model-item>
            <!--Student ID-->
            <a-form-model-item label="Percentage" prop="percentage">
              <a-input v-model="addSubmissionForm.percentage" suffix="%"></a-input>
            </a-form-model-item>
          </a-form-model>
        </div>
      </a-modal>
    </template>
  </div>
</template>

<script>
  import { getTeacherCourses, getSubmissionList } from '../../../api/teacher'
  export default {
    name: 'SubmissionManagement',
    data () {
      var checkPercentage = (rule, value, cb) => {
        const regPercentage = /^([1-9][0-9]{0,1}|100)$/

        if (regPercentage.test(value)) {
          return cb()
        }
        cb(new Error('Please input a valid Student Name'))
      }
      return {
        // list used store all the course info of current teacher
        courseList: [],
        // variable used to indicate the current selected course id
        selectedCourseId: '',
        // variable used to indicate the current selected course name
        selectedCourseName: '',
        // list used to store the submission of course selected
        submissionList: [],
        // columns for the submission list table
        submissionListColumns: [
          {
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
      ],
        // pagination settings for submission list table
        submissionListPagination: {
            // default page size
            defaultPageSize: 5,
            // Show the number of total items
            showTotal: (total) => `Total ${ total } items`,
            total: 0,
            showSizeChanger: true,
            pageSizeOptions: ['5', '10', '15', '20', '25'],
            onShowSizeChange: (current, pageSize) => {
              this.pageNumForSubmission = current
              this.pageSizeForSubmission = pageSize
              this.getSubmissions(this.selectedCourseId)
            },
            onChange: (page, pageSize) => {
              this.pageSizeForSubmission = pageSize
              this.pageNumForSubmission = page
              this.getSubmissions(this.selectedCourseId)
            }
          },
        // current page num for submission list
        pageNumForSubmission: 1,
        // current page size for submission list
        pageSizeForSubmission: 5,
        // variable used to control whether the add submission modal is visible
        addSubmissionModalVisible: false,
        // add submission form
        addSubmissionForm: {
          percentage: '',
          title: '',
          course: '',
          coursename: ''
        },
        addSubmissionRules: {
          percentage: [
            { required: true, message: 'Please input the proposed percentage', trigger: 'blur' },
            { validator: checkPercentage, trigger: 'blur' }
          ]
        },
        // layout settings for the add submission form
        labelCol: { span: 8 },
        wrapperCol: { span: 16 }
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
        }).catch(error => {
          console.info(error)
          this.$notification.error({
            message: 'Error',
            description: 'Failed to get the information of available courses'
          })
        })
      },
      // function used to get the submission list of the current course
      getSubmissions (courseId) {
        getSubmissionList(courseId).then(({ data: response }) => {
          this.submissionList = response.results
          // console.log(response.length)
          this.submissionListPagination.total = response.results.length
          // console.log(this.submissionList)
        }).catch(error => {
          console.info(error)
          this.$notification.error({
            message: 'Error',
            description: 'Failed to get the information of available submissions'
          })
        })
      },
      // function used to get the selected course name
      getCourseName () {
        for (var i = 0; i < this.courseList.length; i++) {
          if (this.courseList[i].id === this.selectedCourseId) {
            this.selectedCourseName = this.courseList[i].title
            console.log(this.selectedCourseName)
          }
        }
      },
      // function executed when user select the target course
      handleChange (value) {
        this.selectedCourseId = value
        this.getCourseName()
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
      },
      // function used to add new submission to the current course
      showAddSubmissionModal () {
        // target course not yet selected
        if (this.selectedCourseId === '') {
          return this.$notification.warn({
            message: 'Warning',
            description: 'Please select the target course before further operations'
          })
        }
        this.addSubmissionForm.coursename = this.selectedCourseName
        this.addSubmissionModalVisible = true
      },
      // function executed when user click submit
      handleAddSubmissionOk () {
      },
      // function used to reset the submission form model
      handleAddStudentModalReset () {
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
