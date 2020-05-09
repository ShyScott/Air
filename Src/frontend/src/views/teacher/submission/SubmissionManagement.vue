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
          <a-select
            placeholder="Please select the course"
            style="width: 400px"
            show-search
            :filterOption="false"
            @search="handleSearch"
            @change="handleChange"
          >
            <a-icon slot="suffixIcon" type="smile" />
            <a-select-option v-for="(item, i) in this.courseList" :key="i" :value="item.id">
              {{ item.title }}
            </a-select-option>
          </a-select>
        </div>
        <!--New submission Button-->
        <div style="margin-top: 20px">
          <a-button type="primary" icon="cloud-upload" size="default" @click="showAddSubmissionModal"> New Submission </a-button>
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
              <a href="#" @click="showEditSubmissionModal(record)"><a-icon type="edit" />Edit</a>
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
        <!--Area prepared for the pie chart-->
        <div style="justify-content: center; display: flex; align-items: center; flex-direction: row">
          <div id="main" style="width: 800px;height:500px; margin-top: 20px;"></div>
        </div>
      </a-card>
      <!--Add Submission Modal-->
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
            ref="addSubmissionFormRef"
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
            <!--Submission Percentage-->
            <a-form-model-item label="Percentage" prop="percentage">
              <a-input v-model="addSubmissionForm.percentage" suffix="%"></a-input>
            </a-form-model-item>
          </a-form-model>
        </div>
      </a-modal>
      <!--Edit Submission Modal-->
      <a-modal v-model="editSubmissionModalVisible" title="Edit Submission" width="800px">
        <template slot="footer">
          <a-button key="Cancel" @click="handleEditSubmissionModalReset">Reset</a-button>
          <a-button key="submit" type="primary" @click="handleEditSubmissionOk">
            Submit
          </a-button>
        </template>
        <div style="width: 640px">
          <a-form-model
            :model="editSubmissionForm"
            :rules="editSubmissionRules"
            ref="editSubmissionFormRef"
            :label-col="labelCol"
            :wrapper-col="wrapperCol">
            <!--Course name-->
            <a-form-model-item label="Course name">
              <a-input v-model="editSubmissionForm.coursename" :disabled="true"></a-input>
            </a-form-model-item>
            <!--Submission Title-->
            <a-form-model-item label="Submission Title" prop="title">
              <a-input v-model="editSubmissionForm.title"></a-input>
            </a-form-model-item>
            <!--Submission Percentage-->
            <a-form-model-item label="Percentage" prop="percentage">
              <a-input v-model="editSubmissionForm.percentage" suffix="%"></a-input>
            </a-form-model-item>
          </a-form-model>
        </div>
      </a-modal>
    </template>
  </div>
</template>

<script>
  import {
    getTeacherCourses,
    getSubmissionList,
    addNewSubmissionToCourse,
    getCoursesByQuery, deleteSubmission, editSubmission
  } from '../../../api/teacher'
  import echarts from 'echarts'
  // import _ from 'lodash'
  export default {
    name: 'SubmissionManagement',
    data () {
      var checkPercentage = (rule, value, cb) => {
        const regPercentage = /^([0-9][0-9]{0,1}|100)$/

        if (regPercentage.test(value)) {
          return cb()
        }
        cb(new Error('Please input a valid percentage'))
      }
      return {
        // parameters for pie chart
        option: {
          title: {
            text: 'Submission Distribution',
            subtext: '',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
          },
          grid: {
            left: '20%'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            data: []
          },
          series: [
            {
              name: 'Source from',
              type: 'pie',
              radius: '55%',
              center: ['50%', '60%'],
              data: [],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        },
        // pie chart data array
        dataArray: [],
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
          // Submission Title column
          title: 'Submission Title',
          dataIndex: 'title',
          width: '35%',
          scopedSlots: { customRender: 'title' }
        },
        {
          // Percentage column
          title: 'Percentage (%)',
          dataIndex: 'percentage',
          width: '30%',
          scopedSlots: { customRender: 'percentage' }
        },
        {
          // operation column
          title: 'Operation',
          dataIndex: 'operation',
          width: '35%',
          scopedSlots: { customRender: 'operation' }
        }
      ],
        // pagination settings for submission list table
        submissionListPagination: {
            current: 1,
            pageSize: 5,
            // Show the number of total items
            showTotal: (total) => `Total ${ total } items`,
            total: 0,
            showSizeChanger: true,
            pageSizeOptions: ['5', '10', '15', '20', '25'],
            onShowSizeChange: (current, pageSize) => {
              this.submissionListPagination.current = current
              this.submissionListPagination.pageSize = pageSize
              this.getSubmissions()
            },
            onChange: (current, pageSize) => {
              this.submissionListPagination.pageSize = pageSize
              this.submissionListPagination.current = current
              this.getSubmissions()
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
          percentage: 0,
          title: '',
          course: ''
        },
        // edit submission form
        editSubmissionForm: {
          percentage: 0,
          title: '',
          course: ''
        },
        // validation rules for add submission form
        addSubmissionRules: {
          percentage: [
            { required: true, message: 'Please input the proposed percentage', trigger: ['change', 'blur'] },
            { validator: checkPercentage, trigger: ['change', 'blur'] }
          ],
          title: [
            { required: true, message: 'Please input the submission title', trigger: 'change' },
            { max: 50, min: 1, message: 'Please input the Submission title with length between 1 and 50', trigger: ['change', 'blur'] }
          ]
        },
        // validation rules for edit submission form
        editSubmissionRules: {
          percentage: [
            { required: true, message: 'Please input the proposed percentage', trigger: ['change', 'blur'] },
            { validator: checkPercentage, trigger: ['change', 'blur'] }
          ],
          title: [
            { required: true, message: 'Please input the submission title', trigger: 'change' },
            { max: 50, min: 1, message: 'Please input the Submission title with length between 1 and 50', trigger: ['change', 'blur'] }
          ]
        },
        // layout settings for the add submission form
        labelCol: { span: 8 },
        wrapperCol: { span: 16 },
        // variable used to control whether to display the edit submission modal
        editSubmissionModalVisible: false,
        // variable used to indicate the submission to be edited
        selectedSubmissionId: '',
        myChart: {},
        // data for chart
        chartDataList: []
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
      getSubmissions () {
        const parameter = {
          course: this.selectedCourseId,
          page: this.submissionListPagination.current,
          size: this.submissionListPagination.pageSize
        }
        getSubmissionList(parameter).then(({ data: response }) => {
          this.submissionList = response.results
          // console.log(response.length)
          this.submissionListPagination.total = response.count
          // console.log(this.submissionList)
          // calculate the data for pie chart
          this.calculateChartData()
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
            // console.log(this.selectedCourseName)
          }
        }
      },
      // function executed when user select the target course
      handleChange (value) {
        this.selectedCourseId = value
        this.getCourseName()
        // console.log(this.selectedCourseId)
        this.getSubmissions()
      },
      // function executed when user click the edit button
      showEditSubmissionModal (course) {
        // console.log(course)
        // give the original values to the edit form
        this.editSubmissionForm.percentage = course.percentage
        this.editSubmissionForm.title = course.title
        this.editSubmissionForm.coursename = this.selectedCourseName
        this.selectedSubmissionId = course.id
        this.editSubmissionModalVisible = true
      },
      // function executed when user confirm to delete the submission
      confirmDeleteSubmission (course) {
        // console.log(course.id)
        deleteSubmission(course.id).then(() => {
          // re-render
          this.getSubmissions()
          // feedback
          return this.$notification.success({
            message: 'Success',
            description: 'Delete the Submission Successful'
          })
        }).catch(error => {
          if (error.response) {
            return this.$notification.error({
              message: 'Error',
              description: 'Delete the Submission Failed'
            })
          }
        })
      },
      // function executed when user cancel the submission delete
      cancelDeleteSubmission () {
        // console.log('cancel')
        return this.$notification.info({
          message: 'Feedback',
          description: 'You have canceled the delete'
        })
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
        this.$refs.addSubmissionFormRef.validate(valid => {
          if (valid) {
            const parameter = { course: this.selectedCourseId, percentage: this.addSubmissionForm.percentage, title: this.addSubmissionForm.title }
            this.addNewSubmission(parameter)
          }
        })
      },
      // function used to reset the submission form model
      handleAddStudentModalReset () {
        this.$refs.addSubmissionFormRef.resetFields()
        this.addSubmissionModalVisible = false
      },
      // function used to add new submission
      addNewSubmission (parameter) {
        addNewSubmissionToCourse(parameter).then(() => {
          // re-render
          this.getSubmissions()
          // reset the form
          this.$refs.addSubmissionFormRef.resetFields()
          // close modal
          this.addSubmissionModalVisible = false
          // give the feedback
          this.$notification.success({
              message: 'Success',
              description: 'Add new submission Successful'
            })
          }
        ).catch(error => {
          // if error occurs
          if (error.response) {
            // console.log(error.response)
            const errorInfo = error.response.data.non_field_errors
            // give the feedback
            return this.$notification.error({
              message: 'Error',
              description: errorInfo[0] + ''
            })
          }
        })
      },
      // when user want to search the target course
      handleSearch (value) {
        // console.log(value)
        const parameter = { title: value }
        getCoursesByQuery(parameter).then(({ data: response }) => {
          // console.log(response)
          this.courseList = response.results
          // console.log(this.courseList)
        })
      },
      // function used to reset the submission form model
      handleEditSubmissionModalReset () {
        this.$refs.editSubmissionFormRef.resetFields()
        this.editSubmissionModalVisible = false
      },
      // function used to edit the submission
      handleEditSubmissionOk () {
        this.$refs.editSubmissionFormRef.validate(valid => {
          if (valid) {
            const parameter = { course: this.selectedCourseId, percentage: this.editSubmissionForm.percentage, title: this.editSubmissionForm.title }
            this.editCurrentSubmission(parameter, this.selectedSubmissionId)
          }
        })
      },
      // function used to edit the given submission
      editCurrentSubmission (parameter, submissionId) {
        editSubmission(parameter, submissionId).then(() => {
            // re-render
            this.getSubmissions()
            // reset the form
            this.$refs.editSubmissionFormRef.resetFields()
            // close modal
            this.editSubmissionModalVisible = false
            // give the feedback
            return this.$notification.success({
              message: 'Success',
              description: 'Edit the submission Successful'
            })
          }
        ).catch(error => {
          // if error occurs
          if (error.response) {
            // console.log(error.response)
            return this.$notification.error({
              message: 'Error',
              description: 'Edit the Submission Failed'
            })
          }
        })
      },
      // function used to calculate the data necessary for the chart
      calculateChartData () {
        getSubmissionList({ course: this.selectedCourseId, page: 1, size: 100 }).then(({ data: response }) => {
          this.chartDataList = response.results
          // console.log(this.chartDataList)
          // clear the former data
          this.option.series[0].data = []
          for (let i = 0; i < this.chartDataList.length; i++) {
            // console.log(i)
            // set legend
            this.option.legend.data.push(this.chartDataList[i].title)
            // set the data used in table
            const object = { value: this.chartDataList[i].percentage, name: this.chartDataList[i].title }
            // console.log(object)
            this.option.series[0].data.push(object)
          }
          // set the subtitle of the chart
          this.option.title.subtext = this.selectedCourseName
          // re-render
          this.myChart.setOption(this.option)
        })
      }
    },
    created () {
      // get all the course info before page rendering
      this.getCourses()
    },
    mounted () {
      // chart initialization
      this.myChart = echarts.init(document.getElementById('main'))
    }
  }
</script>

<style scoped>
  .a-adjust {
    color: red;
    margin-left: 10px;
  }
</style>
