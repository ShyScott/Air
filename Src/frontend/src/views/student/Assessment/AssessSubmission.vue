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
          <a-icon @click="moveToAssessmentManagementPage" type="like"/>
          <span @click="moveToAssessmentManagementPage">Assessment Management</span>
        </a-breadcrumb-item>
        <a-breadcrumb-item href="">
          <a-icon type="solution"/>
          <span>Submission Assessment</span>
        </a-breadcrumb-item>
      </a-breadcrumb>
      <!--Course title-->
      <div style="margin-top: 30px">
        Course Name: <span style="color: #1A8FFF">{{ this.selectedCourseName }}</span>
      </div>
      <a-table style="margin-top: 30px" :dataSource="submissionList" :columns="submissionListColumns" :pagination="submissionListPagination" rowKey="id">
        <template slot-scope="text, record" slot="operation">
          <a-icon style="color: #1A8FFF" type="security-scan"></a-icon>
          <a href="#" @click="showAssessModal(record)"> Assess </a>
        </template>
      </a-table>
    </a-card>
    <!--Assess submission modal-->
    <a-modal width="800px" v-model="assessSubmissionModalVisible" title="Assess Submission" on-ok="handleOk">
      <template slot="footer">
        <a-button key="back" @click="handleCancel">
          Cancel
        </a-button>
        <a-button key="submit" type="primary" @click="handleOk">
          Submit
        </a-button>
      </template>
      <a-form-model
        v-model="assessSubmissionForm"
        ref="assessSubmissionFormRef"
        :label-col="labelCol"
        :wrapper-col="wrapperCol"
      >
        <a-form-model-item label="Submission Title">
          <a-input :disabled="true" v-model="assessSubmissionForm.submissionTitle"></a-input>
        </a-form-model-item>
        <template v-if="this.selectedCourse !== null">
          <a-form-model-item v-for="(item, i) in selectedCourse.team_in.members" :key="i">
            <span style="margin-left: 40px">
              Rate for {{ item.username }} :
              <a-rate :allow-clear="false" :count="4" v-model="assessSubmissionForm.rateForEachOne[i]" :tooltips="desc">
                <a-icon slot="character" type="smile" />
              </a-rate>
              <span class="ant-rate-text">{{ desc[assessSubmissionForm.rateForEachOne[i] - 1] }}</span>
            </span>
          </a-form-model-item>
        </template>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
  import { getCourseInfoById, getSubmissionList, submitAssessmentResults } from '../../../api/student'

  export default {
    name: 'AssessSubmission',
    data () {
      return {
        // current course's id
        selectedCourseId: '',
        // current course' name
        selectedCourseName: '',
        // course selected
        selectedCourse: null,
        // variable used to store all the submissions
        submissionList: [],
        // pagination settings for submissions
        submissionListPagination: {
          current: 1,
          pageSize: 5,
          // Show the number of total items
          showTotal: (total) => `Totally ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '12', '15', '25'],
          onShowSizeChange: (current, pageSize) => {
            this.submissionListPagination.current = current
            this.submissionListPagination.pageSize = pageSize
            this.getSubmission()
          },
          onChange: (current, pageSize) => {
            this.submissionListPagination.pageSize = pageSize
            this.submissionListPagination.current = current
            this.getSubmission()
          }
        },
        // columns settings for the submission list
        submissionListColumns: [
          {
            title: 'Submission Title',
            dataIndex: 'title',
            width: '35%',
            align: 'center',
            scopedSlots: { customRender: 'title' }
          },
          {
            title: 'Submission Percentage (%)',
            dataIndex: 'percentage',
            width: '30%',
            align: 'center',
            scopedSlots: { customRender: 'percentage' }
          },
          {
            title: 'Operation',
            dataIndex: 'operation',
            width: '35%',
            align: 'center',
            scopedSlots: { customRender: 'operation' }
          }
        ],
        // variable used to control the show of assess submission modal
        assessSubmissionModalVisible: false,
        // form object for submission assessment
        assessSubmissionForm: {
          submissionTitle: '',
          rateForEachOne: []
        },
        // layout settings for the add submission form
        labelCol: { span: 5 },
        wrapperCol: { span: 16 },
        // rate description
        desc: ['NONE', 'LITTLE', 'FAIR', 'FULL'],
        // the id of submission selected
        selectedSubmissionId: ''
      }
    },
    methods: {
      // function used to move to main page
      moveToIndex () {
        this.$router.push('mainpage')
      },
      // function used to move to assessment management page
      moveToAssessmentManagementPage () {
        this.$router.push({ name: 'Assessment' })
      },
      // get the submission list of current course
      getSubmission () {
        // process the data
        const parameter = {
          course: this.selectedCourseId,
          page: this.submissionListPagination.current,
          size: this.submissionListPagination.pageSize
        }
        getSubmissionList(parameter).then(({ data: response }) => {
          this.submissionList = response.results
          this.submissionListPagination.total = response.count
          // console.log(this.submissionList)
        }).catch(error => {
          // if error occurs
          if (error.response) {
            this.$notification.error({
              message: 'Error',
              description: 'Failed to get the information of submissions'
            })
          }
        })
      },
      // function used to get the current course's name
      getCourseInfo () {
        getCourseInfoById(this.selectedCourseId).then(({ data: response }) => {
          this.selectedCourseName = response.title
          this.selectedCourse = response
          this.assessSubmissionForm.rateForEachOne = new Array(this.selectedCourse.team_in.members.length).fill(4)
          // console.log(this.selectedCourse)
        })
      },
      // function used to control the show of assess submission modal
      showAssessModal (submission) {
        this.assessSubmissionForm.submissionTitle = submission.title
        this.selectedSubmissionId = submission.id
        this.assessSubmissionModalVisible = true
      },
      // function executed when cancel button is pressed
      handleCancel () {
        this.assessSubmissionForm.rateForEachOne.fill(4)
        this.assessSubmissionModalVisible = false
      },
      // function executed when submit button is pressed
      handleOk () {
        this.submitAssessment()
      },
      // submit assessment for submission
      submitAssessment () {
        // process data
        var parameter = []
        for (let i = 0; i < this.selectedCourse.team_in.members.length; i++) {
          var parameterItem = {
            submission: this.selectedSubmissionId,
            team: this.selectedCourse.team_in.id
          }
          parameterItem.member = this.selectedCourse.team_in.members[i].id
          parameterItem.level = this.assessSubmissionForm.rateForEachOne[i] - 1
          parameter.push(parameterItem)
        }
        // submit to the back end
        submitAssessmentResults(parameter).then(() => {
          this.$notification.success({
            message: 'Success',
            description: 'Submit submission assessment successfully'
          })
          // reset and hide modal
          this.assessSubmissionForm.rateForEachOne.fill(4)
          this.assessSubmissionModalVisible = false
        }).catch(error => {
          if (error.response) {
            this.$notification.error({
              message: 'Error',
              description: 'Failed to submit the assessment'
            })
          }
        })
      }
    },
    created () {
      // store the target course id
      const courseId = this.$route.params.courseId
      this.selectedCourseId = courseId
      this.getSubmission()
      this.getCourseInfo()
    }
  }
</script>

<style scoped>
</style>
