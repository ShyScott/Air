<template>
  <div>
    <a-spin :spinning="this.spinning" size="large">
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
        <!--search bar-->
        <div>
          <a-input-search
            style="margin-top: 20px; width: 50%"
            v-model="courseQuery"
            placeholder="Please input course name"
            @search="getCourses(true)"
            enterButton>
          </a-input-search>
        </div>
        <!--Table Area-->
        <div style="margin-top: 25px">
          <a-table :dataSource="this.courseList" :columns="this.teamInfoTableColumns" rowKey="id" :pagination="this.teaminfolistPagination">
            <template slot="operation" slot-scope="text, record">
              <span v-if="record.is_confirmed === false">
                <!--tooltip for operation button-->
                <a-tooltip placement="top">
                  <template slot="title">
                    <span>Click to do team formation settings</span>
                  </template>
                  <a @click="showFormOptionsModal(record)"><a-icon type="setting" />Form options</a>
                </a-tooltip>
                <!--tooltip for operation button-->
                <a-tooltip>
                  <template slot="title">
                    <span>Click to confirm the team formation of this course</span>
                  </template>
                  <a class="a-adjust" @click="moveToConfirmationPage(record)"><a-icon type="save" />Confirm Teams</a>
                </a-tooltip>
              </span>
              <span v-else>
                <a-tooltip>
                  <template slot="title">
                    <span>Click to view the team distribution</span>
                  </template>
                  <a style="color: goldenrod" @click="showTeamDistributionModal(record)"><a-icon type="apartment" />Team Distribution</a>
                </a-tooltip>
              </span>
            </template>
          </a-table>
        </div>
      </a-card>
      <!--Form option modal-->
      <a-modal v-model="formOptionModalVisible" title="Form Options" width="800px" @cancel="cancelEditFormOptions">
        <!--footer area of the form options modal-->
        <template slot="footer">
          <a-button key="Cancel" @click="cancelEditFormOptions">Cancel</a-button>
          <a-button key="submit" type="primary" @click="handleEditFormOptionsOk">
            Submit
          </a-button>
        </template>
        <!--body area of the form-->
        <div style="width: 640px">
          <a-form-model
            :model="formOptionForm"
            :rules="formOptionFormRules"
            ref="formOptionFormRef"
            :label-col="labelCol"
            :wrapper-col="wrapperCol"
          >
            <!--Course Name-->
            <a-form-model-item label="Course Name">
              <a-input v-model="formOptionForm.coursename" :disabled="true"></a-input>
            </a-form-model-item>
            <!--Form Method-->
            <a-form-model-item label="Forming Method" prop="formMethod">
              <a-select v-model="formOptionForm.formMethod" style="width: 120px">
                <a-select-option :value="1">
                  Method 1
                </a-select-option>
                <a-select-option :value="2">
                  Method 2
                </a-select-option>
                <a-select-option :value="3" :disabled="this.averageGpa === null">
                  Method 3
                </a-select-option>
                <a-select-option :value="4" :disabled="this.currentNum % 2 !== 0">
                  Method 4
                </a-select-option>
                <a-select-option :value="5" :disabled="this.averageGpa === null || this.currentNum % 2 !== 0">
                  Method 5
                </a-select-option>
              </a-select>
            </a-form-model-item>
            <!--alert area-->
            <a-row style="margin-bottom: 20px">
              <a-col :span="8"></a-col>
              <a-col :span="16">
                <a-alert message="Reminder" type="info">
                  <span slot="description" v-html="alertContent" />
                </a-alert>
              </a-col>
            </a-row>
            <!--primary number-->
            <a-form-model-item label="Primary Number" prop="memberCountPrimary">
              <a-input v-model="formOptionForm.memberCountPrimary" :addon-after="teamCountPrimaryText"></a-input>
            </a-form-model-item>
            <!--secondary number-->
            <a-form-model-item label="Secondary Number" prop="memberCountSecondary">
              <a-input v-model="formOptionForm.memberCountSecondary" :addon-after="teamCountSecondaryText"></a-input>
            </a-form-model-item>
            <!--GPA floating band-->
            <a-form-model-item label="GPA Floating Band" prop="gpaFloatingBand">
              <a-input
                :addon-before="prefixOfFloatingBand"
                v-model="formOptionForm.gpaFloatingBand"
                :disabled="formOptionForm.formMethod !== 3 && formOptionForm.formMethod !== 5"
              />
            </a-form-model-item>
          </a-form-model>
        </div>
      </a-modal>
      <!--Team distribution modal-->
      <a-modal v-model="teamDistributionModalVisible" width="800px" title="Team Distribution" on-ok="handTeamDistributionOk">
        <template slot="footer">
          <a-button key="submit" type="primary" @click="handTeamDistributionOk">
            Return
          </a-button>
        </template>
        <a-table :dataSource="teamDistribution" rowKey="id" :columns="teamDistributionColumns" :pagination="teamDistributionPagination">
          <template slot="teamMembers" slot-scope="text, record">
            <span style="margin-right: 15px" v-for="(item, i) in record.members" :key="i">
              {{ item.username }}
            </span>
          </template>
        </a-table>
      </a-modal>
    </a-spin>
  </div>
</template>

<script>
  import {
    getTeacherCourses,
    getMeanGPA,
    changeFormOption,
    queryCourseByName,
    getTeamDistribution
  } from '../../../api/teacher'

  export default {
    name: 'TeamManagement',
    data () {
      const trigger = ['change', 'blur']
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
            align: 'center',
            scopedSlots: { customRender: 'title' }
          },
          {
            title: 'Students Count',
            dataIndex: 'students_count',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'students_count' }
          },
          {
            title: 'Teamed Students Count',
            dataIndex: 'formed_students_count',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'formed_students_count' }
          },
          {
            title: 'Operation',
            dataIndex: 'operation',
            width: '30%',
            align: 'center',
            scopedSlots: { customRender: 'operation' }
          }
        ],
        // pagination settings for team list table
        teaminfolistPagination: {
          current: 1,
          pageSize: 5,
          // Show the number of total items
          showTotal: (total) => `Total ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '15', '20', '25'],
          onShowSizeChange: (current, pageSize) => {
            this.teaminfolistPagination.current = current
            this.teaminfolistPagination.pageSize = pageSize
            // if there is still content left in the search bar
            if (this.courseQuery !== '') {
              // execute function queryCourse instead of getCourses
               return this.queryCourse()
            }
            // re-render
            this.getCourses()
          },
          onChange: (current, pageSize) => {
            this.teaminfolistPagination.current = current
            this.teaminfolistPagination.pageSize = pageSize
            this.getCourses()
          }
        },
        // page num for team table
        pageNumForTeam: 1,
        // page size for team table
        pageSizeForTeam: 5,
        // variable used to control whether the form options modal should be visible or not
        formOptionModalVisible: false,
        // layout settings for the form options form
        labelCol: { span: 8 },
        wrapperCol: { span: 16 },
        // the form object used for the form option
        formOptionForm: {
          coursename: '',
          formMethod: null,
          memberCountPrimary: 1,
          memberCountSecondary: 0,
          teamCountPrimary: 0,
          teamCountSecondary: 0,
          gpaFloatingBand: 0
        },
        // validation rules for the form options form
        formOptionFormRules: {
          formMethod: [
            { required: true, message: 'Please select the forming method', trigger }
          ],
          memberCountPrimary: [
            { required: true, message: 'Please input the primary number', trigger },
            { pattern: /^[1-9]\d*$/, message: 'Please input a positive integer', trigger },
            {
              validator: this.validateTeamNumbers,
              message: 'Please input a valid pair of primary/secondary number!',
              trigger: 'blur'
            }
          ],
          memberCountSecondary: [
            { required: true, message: 'Please input the secondary number', trigger },
            { pattern: /^[0-9]\d*$/, message: 'Please input a natural number', trigger },
            {
              validator: () => {
                this.$refs.formOptionFormRef.validateField(['memberCountPrimary'])
                return true
              },
              message: 'Please input a valid pair of primary/secondary number!',
              trigger: 'blur'
            }
          ],
          gpaFloatingBand: [
            { required: true, message: 'Please input the GPA Floating Band (0 is allowed)', trigger },
            { pattern: /^\d+(\.\d{1,2})?$/, message: 'Please input a non-negative float number with no more than two decimal places', trigger }
          ]
        },
        // the info of course selected currently in the table
        selectedCourseId: '',
        selectedCourseName: '',
        currentNum: 0,
        // average gpa
        averageGpa: 0,
        // the target course of the form options will be changed
        courseToBeEdited: {},
        // the content user input for query
        courseQuery: '',
        // control whether the spinning should be displayed or not
        spinning: false,
        // varibale used to control the show of team distribution table
        teamDistributionModalVisible: false,
        // course to be shown in the team distribution modal
        courseToBeShown: '',
        // page settings for the team distribution modal
        pageNumForTeamDistribution: 1,
        pageSizeForTeamDistribution: 4,
        teamDistributionPagination: {
          // default page size
          defaultPageSize: 4,
          // Show the number of total items
          showTotal: (total) => `Total ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['4', '8', '12'],
          onShowSizeChange: (current, pageSize) => {
            this.pageNumForTeamDistribution = current
            this.pageSizeForTeamDistribution = pageSize
            this.getTeamInfo()
          },
          onChange: (page, pageSize) => {
            this.pageSizeForTeamDistribution = pageSize
            this.pageNumForTeamDistribution = page
            this.getTeamInfo()
          }
        },
        // variable used to store the team list of the selected course
        teamDistribution: [],
        // Columns settings for team distribution modal
        teamDistributionColumns: [
          {
            title: 'Team Name',
            dataIndex: 'name',
            width: '25%',
            align: 'center',
            scopedSlots: { customRender: 'teamName' }
          },
          {
            title: 'Team Members',
            dataIndex: 'members',
            width: '50%',
            align: 'center',
            scopedSlots: { customRender: 'teamMembers' }
          },
          {
            title: 'Members Count',
            dataIndex: 'members.length',
            width: '25%',
            align: 'center',
            scopedSlots: { customRender: 'number' }
          }
        ]
      }
    },
    computed: {
      // The content in the alert area
      alertContent () {
        const val = this.formOptionForm.formMethod
        if (val === null) {
          return `
            When the total number of students in the course is odd, method 4 and 5
            are automatically disabled. <br>
            When there is at least one student in the course whose GPA is not given,
            method 3 and 5 are disabled automatically.
          `
        }
        const messages = {
          1: 'Method 1: All the members are chosen by students themselves',
          2: 'Method 2: The members are decided by system automatically',
          3: 'Method 3: The members are decided by system automatically (GPA will be considered by the system in team formation)',
          4: 'Method 4: A student can choose one friend and others are given by system randomly',
          5: 'Method 5: A student can choose one friend and others are given by system randomly (GPA will be considered by system in team formation)'
        }
        return messages[val]
      },
      // floating band pre-fix
      prefixOfFloatingBand () {
        if (this.averageGpa === null) return ''
        return `${this.averageGpa.toFixed(2)} ±`
      },
      teamCountPrimaryText () {
        return `x ${this.formOptionForm.teamCountPrimary} team(s)`
      },
      teamCountSecondaryText () {
        return `x ${this.formOptionForm.teamCountSecondary} team(s)`
      }
    },
    methods: {
      // function used to move to main page
      moveToIndex () {
        this.$router.push('mainpage')
      },
      // function used to get all the courses
      getCourses (isSearch = false) {
        if (isSearch) this.teaminfolistPagination.current = 1
        const params = {
          page: this.teaminfolistPagination.current,
          size: this.teaminfolistPagination.pageSize
        }
        if (this.courseQuery !== '') params.title = this.courseQuery
        getTeacherCourses(params).then(({ data: response }) => {
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
      // function executed when user click the form options button
      showFormOptionsModal (course) {
        // console.log(course)
        // set the course selected
        this.courseToBeEdited = course
        this.selectedCourseName = course.title
        this.formOptionForm.coursename = this.selectedCourseName
        if (course.form_method !== null) {
          console.log('here')
          this.formOptionForm.formMethod = course.form_method
          this.formOptionForm.memberCountPrimary = course.member_count_primary
          this.formOptionForm.memberCountSecondary = course.member_count_secondary
          this.formOptionForm.gpaFloatingBand = course.floating_band.toFixed(2)
        }
        this.currentNum = course.students_count
        this.validateTeamNumbers()
        this.selectedCourseId = course.id
        // get mean gpa
        getMeanGPA(this.selectedCourseId).then(({ data: response }) => {
          this.averageGpa = response.mean_gpa
        })
        // console.log(this.averageGpa)
        this.formOptionModalVisible = true
      },
      // function executed when user click cancel button on the form options modal
      cancelEditFormOptions () {
        this.$refs.formOptionFormRef.resetFields()
        this.formOptionForm.teamCountPrimary = this.formOptionForm.teamCountSecondary = 0
        this.formOptionModalVisible = false
        console.log('cancel')
      },
      // function executed when user click submit button on the form options modal
      handleEditFormOptionsOk () {
        this.$refs.formOptionFormRef.validate(valid => {
          if (valid) {
            const parameter = {
              title: this.selectedCourseName,
              duration: this.courseToBeEdited.duration,
              form_method: this.formOptionForm.formMethod,
              member_count_primary: parseInt(this.formOptionForm.memberCountPrimary),
              team_count_primary: this.formOptionForm.teamCountPrimary,
              member_count_secondary: parseInt(this.formOptionForm.memberCountSecondary),
              team_count_secondary: this.formOptionForm.teamCountSecondary,
              floating_band: parseFloat(this.formOptionForm.gpaFloatingBand)
            }
            changeFormOption(this.selectedCourseId, parameter).then(({ data: response }) => {
              // console.log(response)
              this.$notification.success({
                message: 'Success',
                description: 'Team formation options submitted successfully'
              })
              this.formOptionModalVisible = false
              if ([2, 3].includes(parameter.form_method)) {
                this.spinning = true
                setTimeout(() => {
                  this.$router.push({ name: 'FormConfirmation', params: { courseId: this.selectedCourseId } })
                }, 2000)
              }
            }).catch(error => {
              // if error occurs
              if (error.response) {
                console.info(error.response)
                let errorInfo = 'Failed to change the form options'
                if (error.response.data) {
                  errorInfo = error.response.data[0]
                  console.log(errorInfo)
                }
                this.$notification.error({
                  message: 'Error',
                  description: errorInfo
                })
              }
            })
          } else {
            console.log(123)
            this.$notification.warn({
              message: 'Warning',
              description: 'Please check your form'
            })
          }
        })
      },
      // function used to validate whether the teacher's proposed team formation is valid or not, also, this function would given recommended formation of primary number and secondary number automatically
      validateTeamNumbers () {
        const validatePairs = (memberCountPrimary, memberCountSecondary) => {
          if (memberCountPrimary <= 0 || memberCountSecondary < 0) return false
          if ([4, 5].includes(this.formOptionForm.formMethod) && (memberCountPrimary < 4 || memberCountPrimary % 2 > 0 || (memberCountSecondary < 4 && memberCountSecondary !== 0) || memberCountSecondary % 2 > 0)) return false
          let teamCountPrimary = Math.floor(this.currentNum / memberCountPrimary)
          for (; teamCountPrimary > 0; --teamCountPrimary) {
            const remain = this.currentNum - teamCountPrimary * memberCountPrimary
            if ((remain === 0 && memberCountSecondary === 0) || (memberCountSecondary > 0 && remain % memberCountSecondary === 0)) {
              this.formOptionForm.teamCountPrimary = teamCountPrimary
              this.formOptionForm.memberCountSecondary = memberCountSecondary
              const teamCountSecondary = remain === 0 ? 0 : Math.floor(remain / memberCountSecondary)
              this.formOptionForm.teamCountSecondary = teamCountSecondary
              if (teamCountSecondary === 0) this.formOptionForm.memberCountSecondary = 0
              return true
            }
          }
          return false
        }

        const memberCountPrimary = parseInt(this.formOptionForm.memberCountPrimary)
        const memberCountSecondary = parseInt(this.formOptionForm.memberCountSecondary)
        if (validatePairs(memberCountPrimary, memberCountSecondary)) return true

        const step = this.formOptionForm.formMethod >= 4 ? 2 : 1
        let delta = step
        while (true) {
          const flag1 = memberCountPrimary + delta <= this.currentNum
          const flag2 = memberCountPrimary - delta > 0
          if (flag1 || flag2) {
            if (flag1 && validatePairs(memberCountPrimary, memberCountPrimary + delta)) return true
            if (flag2 && validatePairs(memberCountPrimary, memberCountPrimary - delta)) return true
          } else {
            return false
          }
          delta += step
        }
      },
      // function used to routes to the confirmation page after user submit form options or click the confirm button
      moveToConfirmationPage (course) {
        // console.log(course)
        this.selectedCourseId = course.id
        // console.log(this.selectedCourseId)
        this.$router.push({ name: 'FormConfirmation', params: { courseId: this.selectedCourseId } })
      },
      // function executed for the course query
      queryCourse () {
        // console.log(this.courseQuery)
        const parameter = { title: this.courseQuery, page: this.pageNumForTeam, size: this.pageSizeForTeam }
        queryCourseByName(parameter).then(({ data: response }) => {
          // console.log(response)
          this.courseList = response.results
          this.teaminfolistPagination.total = response.count
        })
      },
      // function used to control the show of team distribution modal
      showTeamDistributionModal (course) {
        // console.log(course)
        this.courseToBeShown = course.id
        this.getTeamInfo()
        this.teamDistributionModalVisible = true
      },
      // function executed when user click the return button in the team distribution modal
      handTeamDistributionOk () {
        this.teamDistributionModalVisible = false
      },
      // function used to get all the teams of one course
      getTeamInfo () {
        const parameter = { course: this.courseToBeShown, page: this.pageNumForTeamDistribution, size: this.pageSizeForTeamDistribution }
        getTeamDistribution(parameter).then(({ data: response }) => {
          this.teamDistribution = response.results
          this.teamDistributionPagination.total = response.count
          console.log(response)
        }).catch(error => {
          if (error.response) {
            console.info(error.response)
            return this.$notification.error({
              message: 'Error',
              description: 'Failed to get the team distribution'
            })
          }
        })
      }
    },
    created () {
      this.getCourses()
    }
  }
</script>

<style scoped>
  .a-adjust {
    color: red;
    margin-left: 20px;
  }
</style>
