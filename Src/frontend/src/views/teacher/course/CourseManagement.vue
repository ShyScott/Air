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
          <a-icon type="read"/>
          <span>Course Management</span>
        </a-breadcrumb-item>
      </a-breadcrumb>
      <a-button class="addButton-adjust" type="primary" size="default" @click="MoveToAddCoursePage">
        <a-icon type="coffee"/>
        New Course
      </a-button>
      <!--Alert Area-->
      <a-alert style="margin-top: 20px" message="Reminder: Please click the course name for students management" type="info" showIcon />
      <!--The table of courses-->
      <a-table class="table-adjust" :columns="this.courseColumns" :dataSource="courseList" rowKey="id" :pagination="paginationForCourseTable">
        <template slot="name" slot-scope="text, record">
          <a @click="DisplayInfoOnStudentManageCard(record)">{{ record.title }}</a>
          <span v-if="record.is_confirmed === true"><a-icon style="color: red; margin-left: 10px" type="lock"></a-icon></span>
          <span v-else><a-icon style="color: goldenrod; margin-left: 10px" type="unlock"></a-icon></span>
        </template>
        <!--operation area of the table-->
        <template slot="operation" slot-scope="text, record">
          <!--tooltip for operation button-->
          <a-tooltip placement="top">
            <template slot="title">
              <span>Click to edit this course</span>
            </template>
            <a href="#" @click="moveToCourseInfoEditPage(record)"><a-icon type="edit" />Edit</a>
          </a-tooltip>
          <a-popconfirm title="Are you sure to delete this course?" @confirm="ConfirmCourseDelete(record.id)" @cancel="CancelCourseDelete">
            <!--tooltip for operation button-->
            <a-tooltip>
              <template slot="title">
                <span>Click to delete this course</span>
              </template>
              <a class="a-adjust" href="#" style="font-color: red"><a-icon type="delete" />Delete</a>
            </a-tooltip>
          </a-popconfirm>
        </template>
      </a-table>
    </a-card>
    <!--Student management card area-->
    <a-card title="Course Info" style="margin-top: 20px">
      Chosed Course: {{ this.studentManagementForm.chosedCourse }}
      <a-form>
        <a-form-item style="margin-bottom: 5px">
          <div>
            <a-input-search style="margin-top: 20px; width: 50%" v-model="studentListQuery" placeholder="Please input student name" @search="QueryStudent" enterButton></a-input-search>
          </div>
        </a-form-item>
      </a-form>
      <div style="margin-bottom: 20px">
        <a-button
          class="addButton-adjust"
          type="primary"
          size="default"
          style="margin-right: 20px"
          :disabled="this.isSelectedCourseConfirmed === true"
          @click="ShowAddStudentModal">
          <a-icon type="user-add"/>
          Add a Student
        </a-button>
        <a-button class="addButton-adjust" type="primary" size="default" :disabled="this.isSelectedCourseConfirmed === true">
          <a-icon type="file-done"/>
          Import students from a file
        </a-button>
      </div>
      <a-table :columns="studentListColumns" :dataSource="studentList" rowKey="id" :pagination="paginationForStudentListTable">
        <!--Add delete button to operation slot-->
        <template slot="operation" slot-scope="text, record">
          <!--Operation Area-->
          <a-popconfirm title="Are you sure to remove this student from the course?" @confirm="ConfirmStudentRemove(selectedCourseId, record.id)" @cancel="CancelStudentRemove">
            <a-tooltip>
              <template slot="title">
                <span>Click to delete the student from this course</span>
              </template>
              <a class="a-adjust" href="#" style="font-color: red"><a-icon type="delete" />Remove</a>
            </a-tooltip>
          </a-popconfirm>
        </template>
      </a-table>
    </a-card>
    <a-modal v-model="addStudentModalVisible" title="Add a Student" onOk="handleAddStudentModalOk" width="800px">
      <template slot="footer">
        <a-button key="Cancel" @click="handleAddStudentModalReset">Reset</a-button>
        <a-button key="submit" type="primary" @click="handleAddStudentModalOk">
          Submit
        </a-button>
      </template>
      <div style="width: 640px">
        <a-form-model
          :model="addStudentForm"
          :rules="addStudentFormRules"
          ref="addStudentFormRef"
          :label-col="labelCol"
          :wrapper-col="wrapperCol">
          <!--Course name-->
          <a-form-model-item label="Course name">
            <a-input v-model="this.addStudentForm.coursename" :disabled="true"></a-input>
          </a-form-model-item>
          <!--Student name-->
          <a-form-model-item label="Student name" prop="username">
            <a-input v-model="addStudentForm.username"></a-input>
          </a-form-model-item>
          <!--Student ID-->
          <a-form-model-item label="Student ID" prop="student_id">
            <a-input v-model="addStudentForm.student_id"></a-input>
          </a-form-model-item>
          <!--Email-->
          <a-form-model-item label="Email" prop="email">
            <a-input v-model="addStudentForm.email"></a-input>
          </a-form-model-item>
          <!--GPA-->
          <a-form-model-item label="GPA" prop="gpa">
            <a-input v-model="addStudentForm.gpa"></a-input>
          </a-form-model-item>
          <!--default password-->
          <a-form-model-item label="Default Password" prop="default_password">
            <a-input v-model="addStudentForm.default_password"></a-input>
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { getTeacherCourses, getCourseInfoById, getStudentListOfTheCourse, getStudentByQuery, deleteCourse, removeStudent, addStudentToTheCourse } from '../../../api/teacher'
  import { mapGetters } from 'vuex'
  import pick from 'lodash.pick'

  export default {
    name: 'CourseManagement',
    data () {
      // Email address validator
      var checkEmail = (rule, value, cb) => {
        const regEmail = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z-Z0-9_-])+/

        if (regEmail.test(value)) {
          return cb()
        }

        cb(new Error('Please input a valid Email Address'))
      }
      // GPA format validator
      var checkGPA = (rule, value, cb) => {
        if (value === '') return cb()

        const regFloat = /^\d+(.\d{1,2})?$/
        if (!regFloat.test(value)) {
          return cb(new Error('Please input a float number with no more than 2 decimal places'))
        }

        const gpa = parseFloat(value)
        const eps = 0.001
        if (gpa - 0 < eps || gpa - 4 > eps) {
          return cb(new Error('Please input a valid GPA'))
        }

        return cb()
      }
      // student name format validator
      var checkStudentName = (rule, value, cb) => {
        const regName = /^[A-Za-z]*(\s[A-Za-z]*)*$/

        if (regName.test(value)) {
          return cb()
        }

        cb(new Error('Please input a valid Student Name'))
      }
      return {
        // Used to indicate the header of the course table
        courseColumns: [{
          // Course name column
          title: 'Course Name',
          dataIndex: 'title',
          width: '30%',
          align: 'center',
          scopedSlots: { customRender: 'name' }
        },
          {
            // Duration column
            title: 'Duration',
            dataIndex: 'duration',
            width: '25%',
            align: 'center',
            scopedSlots: { customRender: 'duration' }
          },
          {
            // Student number column
            title: 'Number',
            dataIndex: 'students_count',
            width: '25%',
            align: 'center',
            scopedSlots: { customRender: 'students_count' }
          },
          {
            // operation column
            title: 'Operation',
            dataIndex: 'operation',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'operation' }
          }
        ],
        // Columns settings for the student list table in the student management card
        studentListColumns: [
          {
            // Student name column
            title: 'Student Name',
            dataIndex: 'username',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'username' }
          },
          {
            // Email column
            title: 'Email Address',
            dataIndex: 'student_profile.email',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'email' }
          },
          {
            // Student ID column
            title: 'Student ID',
            dataIndex: 'student_profile.student_id',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'id' }
          },
          {
            // GPA column
            title: 'GPA',
            dataIndex: 'student_profile.gpa',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'gpa' }
          },
          {
            // operation column
            title: 'Operation',
            dataIndex: 'operation',
            width: '20%',
            align: 'center',
            scopedSlots: { customRender: 'operation' }
          }
        ],
        // list used to store all the courses of current teacher
        courseList: [],
        // list used to store all the students taking the course selected
        studentList: [],
        // object used to adjust the pagination of the course table
        paginationForCourseTable: {
          // default page size
          defaultPageSize: 5,
          // Show the number of total items
          showTotal: (total) => `Totally ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '12', '15', '25'],
          onShowSizeChange: (current, pageSize) => {
            this.pagenumForCourse = current
            this.pagesizeForCourse = pageSize
            this.getCourses()
          },
          onChange: (page, pageSize) => {
            this.pagesizeForCourse = pageSize
            this.pagenumForCourse = page
            // console.log(this.pagesizeForCourse)
            // console.log(this.pagenumForCourse)
            this.getCourses()
          }
        },
        // object used to adjust the pagination of the student list table
        paginationForStudentListTable: {
          // default page size
          defaultPageSize: 5,
          // Show the number of total items
          showTotal: (total) => `Totally ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '15', '20', '25'],
          onShowSizeChange: (current, pageSize) => {
            this.pagenumForStudentList = current
            this.pagesizeForStudentList = pageSize
            // if search bar has been input something, do not run the function getStudentList
            if (this.studentListQuery) {
              getStudentByQuery(this.studentListQuery, this.selectedCourseId).then(({ data: response }) => {
                this.studentList = response.results
                // pagination settings
                this.totalForStudentList = response.count
                this.paginationForStudentListTable.total = response.count
                // console.log(response)
              })
            } else {
              this.getStudentList(this.selectedCourseId)
            }
          },
          onChange: (page, pageSize) => {
            this.pagesizeForStudentList = pageSize
            this.pagenumForStudentList = page
            // if search bar has been input something, do not run the function getStudentList
            if (this.studentListQuery) {
              getStudentByQuery(this.studentListQuery, this.selectedCourseId).then(({ data: response }) => {
                this.studentList = response.results
                // pagination settings
                this.totalForStudentList = response.count
                this.paginationForStudentListTable.total = response.count
                // console.log(response)
              })
            } else {
              this.getStudentList(this.selectedCourseId)
            }
          }
        },
        // Form object used in the students management
        studentManagementForm: {
          chosedCourse: ''
        },
        // The query info input by the user
        studentListQuery: '',
        // the id of the course selected by user
        selectedCourseId: '',
        // pagination parameters for the course table
        totalForCourse: 0,
        pagenumForCourse: 1,
        pagesizeForCourse: 5,
        // pagination parameters for the student list table
        totalForStudentList: 0,
        pagenumForStudentList: 1,
        pagesizeForStudentList: 5,
        // variable used to control whether the add student modal is visible or not
        addStudentModalVisible: false,
        // form object used to add the student
        addStudentForm: {
          username: '',
          coursename: '',
          student_id: '',
          email: '',
          gpa: '',
          default_password: ''
        },
        // layout settings for the add student form
        labelCol: { span: 8 },
        wrapperCol: { span: 16 },
        // validation rules for the add student form
        addStudentFormRules: {
          // validation for username
          username: [
            { required: true, message: `Please input the student's name`, trigger: 'blur' },
            { validator: checkStudentName, trigger: 'blur' }
          ],
          student_id: [
            { required: true, message: `Please input the student's ID`, trigger: 'blur' }
          ],
          email: [
            { required: true, message: `Please input the student's Email Address`, trigger: 'blur' },
            { validator: checkEmail, trigger: 'blur' }
          ],
          gpa: [
            { validator: checkGPA, trigger: 'blur' }
          ],
          default_password: [
            { required: true, message: 'Please input the default password', trigger: 'blur' }
          ]
        },
        // variable used to indicate whether the course selected is confirmed
        isSelectedCourseConfirmed: false
      }
    },
    computed: {
      // get current Teacher's information via vuex
      ...mapGetters([
        'nickname'
      ])
    },
    methods: {
      // function used to move to main page
      moveToIndex () {
        this.$router.push('mainpage')
      },
      // function used to get all the courses available of current Teacher
      getCourses () {
        getTeacherCourses(this.pagenumForCourse, this.pagesizeForCourse).then(({ data: response }) => {
          // console.log(response)
          this.courseList = response.results
          // pagination settings
          this.totalForCourse = response.count
          this.paginationForCourseTable.total = response.count
          // console.log(this.totalForCourse)
          // console.log(this.courseList)
          }
        ).catch(error => {
          console.info(error)
          this.$notification.error({
            message: 'Error',
            description: 'Failed to get the information of available courses'
          })
        })
      },
      // get the information of the course selected to be edited
      getCourseInfoToBeEdited (id) {
        // console.log(id)
        getCourseInfoById(id).then(response => {
          this.courseInfoEditForm = response.data
          // console.log(this.courseInfoEditForm)
        }).catch(error => {
          console.info(error)
          // if failing, output the warning message
          this.$notification.error({
            message: 'Error',
            description: 'Failed to get the information of selected course'
          })
        })
      },
      // get the students list according to the course id given
      getStudentList (courseId) {
        getStudentListOfTheCourse(courseId, this.pagenumForStudentList, this.pagesizeForStudentList).then(({ data: response }) => {
          this.studentList = response.results
          // pagination settings
          this.totalForStudentList = response.count
          this.paginationForStudentListTable.total = response.count
          // console.log(this.studentList)
        })
      },
      // function used to fill the infomation supposed to be displayed in the Student Managemet Card
      // course is the info of course selected
      DisplayInfoOnStudentManageCard (course) {
        this.studentManagementForm.chosedCourse = course.title
        // console.log(course.id)
        this.selectedCourseId = course.id
        // check if the course is confirmed
        if (course.is_confirmed === true) {
          this.isSelectedCourseConfirmed = true
        } else {
          this.isSelectedCourseConfirmed = false
        }
        // console.log(this.selectedCourseId)
        this.getStudentList(this.selectedCourseId)
        this.studentListQuery = ''
      },
      // function used to show the course info edit modal
      moveToCourseInfoEditPage (course) {
        // console.log(course.id)
        const target = { name: 'AddCourse' }
        this.$router.push(target)
      },
      // function used to query the student info input by the user
      QueryStudent () {
        // if course is not selected yet
        // give the warning
        if (this.selectedCourseId === '') {
          return this.$notification.info({
            message: 'Reminder',
            description: 'Please select the target course before searching'
          })
        }
        // judge if user has input something
        // if nothing, search by course id
        if (this.studentListQuery === '') {
          // console.log('Nothing')
          this.getStudentList(this.selectedCourseId)
        }
        // if all the query info available, do the searching
        getStudentByQuery(this.studentListQuery, this.selectedCourseId).then(({ data: response }) => {
          this.studentList = response.results
          // pagination settings
          this.totalForStudentList = response.count
          this.paginationForStudentListTable.total = response.count
          // console.log(response)
        })
      },
      // function executed when user confirm to delete the course
      ConfirmCourseDelete (courseId) {
        // console.log(courseId)
        deleteCourse(courseId).then(() => {
          // solve the problem: if there is only 1 student left in the current page, delete this course will lead to a 404 since that current page is not existed anymore
          if (this.totalForCourse % this.pagesizeForCourse === 1) {
            this.pagenumForCourse -= 1
          }
          // re-render
          this.getCourses()
          // this.getStudentList(this.selectedCourseId)
          this.$notification.success({
            message: 'Message',
            description: 'Course delete Successful'
          })
        }).catch(error => {
          if (error.response) {
            this.$notification.error({
              message: 'Message',
              description: 'Course delete Failed'
            })
          }
          }
        )
      },
      // function executed when user cancel to delete the course
      CancelCourseDelete () {
        this.$notification.info({
          message: 'Message',
          description: 'You have canceled the course delete'
        })
      },
      // function executed when user confirm to remove the student from the course
      ConfirmStudentRemove (courseId, studentId) {
        // console.log(courseId)
        // console.log(studentId)
        removeStudent(courseId, studentId).then(() => {
          // solve the problem: if there is only 1 student left in the current page, remove this student will lead to a 404 since that current page is not existed anymore
          if (this.totalForStudentList % this.pagesizeForStudentList === 1) {
            this.pagenumForStudentList -= 1
          }
          // re-render 2 tables
          this.getCourses()
          this.getStudentList(this.selectedCourseId)
          this.$notification.success({
            message: 'Message',
            description: 'Student remove Successful'
          })
        }).catch(error => {
            if (error.response) {
              console.log(error.response)
              this.$notification.error({
                message: 'Message',
                description: 'Student remove Failed'
              })
            }
          }
        )
      },
      // function executed when user cancel to remove the student from student list
      CancelStudentRemove () {
        this.$notification.info({
          message: 'Message',
          description: 'You have canceled the student remove'
        })
      },
      // function used to show the Add student modal
      ShowAddStudentModal () {
        // make sure teacher has picked a course before add the student
        if (this.selectedCourseId === '') {
          return this.$notification.warn(
            {
              message: 'Warning',
              description: 'Please select the target course firstly'
            }
          )
        }
        this.addStudentForm.coursename = this.studentManagementForm.chosedCourse
        this.addStudentModalVisible = true
      },
      // function executed when user click the cancel button of the add student modal
      handleAddStudentModalReset () {
        // clear all the input when canceling
        this.$refs.addStudentFormRef.resetFields()
        this.addStudentModalVisible = false
      },
      // function executed when user click the submit button of the add student modal
      handleAddStudentModalOk () {
        this.$refs.addStudentFormRef.validate(valid => {
          // if all the info user input has past the validation
          if (valid) {
            const profile = pick(this.addStudentForm, ['student_id', 'email', 'gpa'])
            if (profile.gpa === '') delete profile.gpa
            const parameter = {
              students: [
                {
                  username: this.addStudentForm.username,
                  student_profile: profile
                }
              ],
              course: this.selectedCourseId,
              default_password: this.addStudentForm.default_password
            }
            addStudentToTheCourse(parameter).then(() => {
              this.getStudentList(this.selectedCourseId)
              this.getCourses()
              this.addStudentModalVisible = false
              this.$refs.addStudentFormRef.resetFields()
              return this.$notification.success({
                message: 'Message',
                description: 'Add new student Successful'
              })
            }).catch(error => {
              console.info(error)
              return this.$notification.error({
                message: 'Message',
                description: 'Add new student Failed'
              })
            })
          } else {
            return this.$notification.warn({
              message: 'Message',
              description: 'Please provide valid information for submit'
            })
          }
        })
      },
      // function used to route to the add course page
      MoveToAddCoursePage () {
        const target = { name: 'AddCourse' }
        this.$router.push(target)
      }
    },
    created () {
      // get all the courses belonging to the current teacher after initialzaion
      this.getCourses()
    }
  }
</script>

<style lang="less" scoped>
  .addButton-adjust {
    margin-top: 20px;
    font-size: 15px;
  }

  .table-adjust {
    margin-top: 25px;
  }

  .a-adjust {
    margin-left: 20px;
    color: #EE2C2C;
  }

  .highlight {
    background-color: rgb(255, 192, 105);
    padding: 0px;
  }
</style>
