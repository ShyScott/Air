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
    <!--Form option moda-->
    <a-modal v-model="this.formOptionModalVisible" title="Form Options" width="800px">
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
          <a-form-model-item label="Forming Method" prop="form_method">
            <a-select default-value="" style="width: 120px" @change="setFormingMethod">
              <a-select-option value="1">
                Method 1
              </a-select-option>
              <a-select-option value="2">
                Method 2
              </a-select-option>
              <a-select-option value="3">
                Method 3
              </a-select-option>
              <a-select-option value="4" :disabled="(this.currentNum % 2) === 0 ? false : true">
                Method 4
              </a-select-option>
              <a-select-option value="5" :disabled="(this.currentNum % 2) === 0 ? false : true">
                Method 5
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <!--alert area-->
          <a-row style="margin-bottom: 20px">
            <a-col :span="8"></a-col>
            <a-col :span="16">
              <a-alert message="Reminder" type="info">
                <p slot="description">
                  {{ this.alertContent }}
                </p>
              </a-alert>
            </a-col>
          </a-row>
          <!--primary number-->
          <a-form-model-item label="Primary Number" prop="primary_number">
            <a-input v-model="formOptionForm.primary_number"></a-input>
          </a-form-model-item>
          <!--secondary number-->
          <a-form-model-item label="Secondary Number" prop="secondary_number">
            <a-input v-model="formOptionForm.secondary_number"></a-input>
          </a-form-model-item>
          <!--GPA floating band-->
          <a-form-model-item label="GPA Floating Band" prop="gpa_floating_band">
            <!--TODO The adjustment of prefix-->
            <a-input class="input-adjust" :prefix="this.prefixOfFloatingBand" v-model="formOptionForm.gpa_floating_band"></a-input>
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { getTeacherCourses, getTeamsList, getMeanGPA } from '../../../api/teacher'
  export default {
    name: 'TeamManagement',
    data () {
      // validation for positive integer
      const checkInteger = (rule, value, cb) => {
        const regInteger = /^[1-9]\d*$/

        if (regInteger.test(value)) {
          return cb()
        }
        cb(new Error('Please input a positive integer'))
      }
      // validation for positive real number
      // TODO
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
        pageSizeForTeam: 5,
        // variable used to control whether the form options modal should be visible or not
        formOptionModalVisible: false,
        // layout settings for the form options form
        labelCol: { span: 8 },
        wrapperCol: { span: 16 },
        // the form object used for the form option
        formOptionForm: {
          coursename: '',
          form_method: '',
          primary_number: 0,
          secondary_number: 0,
          gpa_floating_band: 0
        },
        // validation rules for the form options form
        formOptionFormRules: {
          form_method: [
            { required: true, message: 'Please select the forming method', trigger: ['change', 'blur'] }
          ],
          primary_number: [
            { required: true, message: 'Please input the primary number', trigger: 'blur' },
            { validator: checkInteger, trigger: ['change', 'blur'] }
          ],
          secondary_number: [
            { required: true, message: 'Please input the secondary number', trigger: 'blur' },
            { validator: checkInteger, trigger: ['change', 'blur'] }
          ],
          gpa_floating_band: [
            { required: true, message: 'Please input the GPA Floating Band (0 is allowed)', trigger: ['blur', 'change'] }
          ]
        },
        // the info of course selected currently in the table
        selectedCourseId: '',
        selectedCourseName: '',
        currentNum: 0,
        // The content in the alert area
        // default content
        alertContent: 'When the total number of students in the course is odd, method 4 and 5 are automatically disabled.',
        // average gpa
        averageGpa: 0,
        // floating band pre-fix
        prefixOfFloatingBand: '0 ±'
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
        // console.log(course)
        // set the course selected
        this.selectedCourseName = course.title
        this.formOptionForm.coursename = this.selectedCourseName
        this.currentNum = course.students_count
        this.selectedCourseId = course.id
        // get mean gpa
        getMeanGPA(this.selectedCourseId).then(({ data: response }) => {
          this.averageGpa = response.mean_gpa
          this.prefixOfFloatingBand = this.averageGpa.toFixed(2) + '±'
        })
        // console.log(this.averageGpa)
        this.formOptionModalVisible = true
      },
      // function executed when user click cancel button on the form options modal
      cancelEditFormOptions () {
        this.$refs.formOptionFormRef.resetFields()
        this.formOptionModalVisible = false
        console.log('cancel')
      },
      // function executed when user click submit button on the form options modal
      handleEditFormOptionsOk () {
        this.formOptionModalVisible = false
        console.log('submit')
      },
      // function used to set the forming method user select
      setFormingMethod (value) {
        this.formOptionForm.form_method = value
        // console.log(value)
        // set the alert content
        if (this.formOptionForm.form_method === '1') {
          this.alertContent = 'Method 1: All the members are chosen by students themselves'
        }
        if (this.formOptionForm.form_method === '2') {
          this.alertContent = 'Method 2: The members are decided by system automatically'
        }
        if (this.formOptionForm.form_method === '3') {
          this.alertContent = 'Method 3: A student can choose one friend and others are given by system randomly'
        }
        if (this.formOptionForm.form_method === '4') {
          this.alertContent = 'Method 4: The members are decided by system automatically (GPA will be considered by the system in team formation)'
        }
        if (this.formOptionForm.form_method === '5') {
          this.alertContent = 'Method 5: A student can choose one friend and others are given by system randomly (GPA will be considered by system in team formation)'
        }
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
