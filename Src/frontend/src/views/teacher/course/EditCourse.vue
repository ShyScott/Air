<template>
  <a-card :title="cardTitle">
    <a-button slot="extra" type="primary" @click="save">Save</a-button>
    <a-form-model v-bind="formLayout" ref="editCourseFormRef" :model="editCourseForm" :rules="editCourseFormRules">
      <a-tabs :defaultActiveKey="defaultActiveKey">
        <!--Tab 1 used to register common course information-->
        <a-tab-pane v-if="mode & 1" :key="1">
          <span slot="tab">
            <a-icon type="idcard" />
            Course Info
          </span>

          <!--Course name-->
          <a-form-model-item label="Course Name" style="width: 850px; margin-top: 20px" prop="title">
            <a-input v-model="editCourseForm.title"></a-input>
          </a-form-model-item>
          <!--duration given by the system-->
          <a-form-model-item label="Duration" style="width: 850px">
            <a-input :value="duration" :disabled="true"></a-input>
          </a-form-model-item>
        </a-tab-pane>

        <!-- Tab 2 used to import student list by file-->
        <a-tab-pane v-if="mode & 2" :key="2">
          <span slot="tab">
            <a-icon type="usergroup-add" />
            Import Students
          </span>

          <a-form-model-item label="Students Info File" style="width: 850px">
            <a-upload-dragger
              accept=".xls, .xlsx"
              :fileList="fileList"
              :remove="removeFile"
              :beforeUpload="() => false"
              @change="fileListChange"
              @reject="rejectFilesNotAccept"
            >
              <p class="ant-upload-drag-icon">
                <a-icon type="inbox" />
              </p>
              <p class="ant-upload-text">Click or drag file to this area to import students</p>
            </a-upload-dragger>
          </a-form-model-item>
          <a-form-model-item label="Default Password" style="width: 850px" prop="default_password">
            <a-input v-model="editCourseForm.default_password"></a-input>
          </a-form-model-item>
          <a-alert
            v-if="studentsInfoHasError"
            style="margin-top: 16px"
            type="warning"
            message="Warning"
            showIcon
          >
            <template slot="description">
              <span>
                Some students' info contain errors. Please check the values in
                <span style="font-weight: bold; color: red">red</span>
                in the table below.
              </span>
              <br>
              <span>Rows with red values will not be imported.</span>
            </template>
          </a-alert>
          <a-table
            style="margin-top: 16px"
            size="middle"
            rowKey="username"
            :dataSource="tableData"
            :pagination="studentListPagination"
          >
            <a-table-column
              v-for="col in studentListColumns"
              :key="col.dataIndex"
              :title="col.title"
              :dataIndex="col.dataIndex"
            >
              <template slot-scope="text">
                <span :style="col.validator(text) ? {} : { fontWeight: 'bold', color: 'red' }">{{ text }}</span>
              </template>
            </a-table-column>
          </a-table>
        </a-tab-pane>
      </a-tabs>
    </a-form-model>
  </a-card>
</template>

<script>
  import { convertDuration } from '@/utils/util'
  import { createCourse, editCourse, importStudents } from '@/api/teacher'
  import XLSX from 'xlsx'
  import pick from 'lodash.pick'
  import { mapGetters } from 'vuex'
  import moment from 'moment'

  export default {
    name: 'EditCourse',
    data () {
      // course info validators
      const validateDefaultPassword = (rule, value, cb) => {
        if (this.mode === 1) return cb()
        if (value === '') return cb(new Error('Please input default password'))
        return cb()
      }

      // student info validators
      const validateUserName = value => {
        const reg = /^[A-Za-z]+( +[A-Za-z]+)*$/
        return reg.test(value) && value.length <= 150
      }
      const validateEmail = value => {
        const reg = /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/
        return reg.test(value)
      }
      const validateStudentId = value => String(value).length > 0
      const validateGPA = value => {
        if (value === '') return true
        const reg = /^\d+(.\d{1,2})?$/
        if (!reg.test(value)) return false
        const gpa = parseFloat(value)
        return gpa >= 0 || gpa <= 4
      }

      return {
        // default active key for the tab-panel
        defaultActiveKey: 1,
        // form layout settings
        formLayout: {
          labelCol: { span: 4 },
          wrapperCol: { span: 16 }
        },
        // course duration
        duration: '',
        // form object used to edit course
        editCourseForm: {
          title: '',
          default_password: ''
        },
        // validation rules for course add
        editCourseFormRules: {
          title: [
            { required: true, max: 128, message: 'Please input course name with no more than 128 characters', trigger: 'blur' }
          ],
          default_password: [
            { validator: validateDefaultPassword, trigger: 'blur' }
          ]
        },
        // file list of the file uploader
        fileList: [],
        // imported students info
        studentsInfo: [],
        // flag to notify user if students info has error
        studentsInfoHasError: false,
        // used to store the student list imported from the table
        tableData: [],
        // columns of the student list table
        studentListColumns: [
          {
            // Student name column
            title: 'Student Name',
            dataIndex: 'username',
            keyword: 'name',
            optional: false,
            validator: validateUserName
          },
          {
            // Email column
            title: 'Email Address',
            dataIndex: 'email',
            keyword: 'mail',
            optional: false,
            validator: validateEmail
          },
          {
            // Student ID column
            title: 'Student ID',
            dataIndex: 'student_id',
            keyword: 'id',
            optional: false,
            validator: validateStudentId
          },
          {
            // GPA column
            title: 'GPA',
            dataIndex: 'gpa',
            keyword: 'gpa',
            optional: true,
            validator: validateGPA
          }
        ],
        // object used to adjust the pagination of the student list table
        studentListPagination: {
          current: 1,
          pageSize: 5,
          total: 0,
          // Show the number of total items
          showTotal: (total) => `Total ${total} items`,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '15', '20', '25'],
          onShowSizeChange: this.previewStudentsInfo,
          onChange: this.previewStudentsInfo
        }
      }
    },
    computed: {
      cardTitle () {
        if (this.mode === 3) return 'Add a new course'
        return 'Edit course - ' + this.selectedCourse.title
      },
      ...mapGetters({
        mode: 'editCourseMode',
        selectedCourse: 'selectedCourse'
      })
    },
    created () {
      // initialize page according to mode
      if (this.mode === 2) this.defaultActiveKey = 2
      if (this.mode < 3) {
        this.editCourseForm.title = this.selectedCourse.title
      }

      // initialize duration
      this.duration = convertDuration(this.mode < 3 ? moment(this.selectedCourse.duration) : moment())
    },
    methods: {
      // file upload change handler
      fileListChange (info) {
        this.fileList = info.fileList.splice(-1)
        if (this.fileList.length) this.importFile(this.fileList[0])
      },
      // function used to reject files that not accept
      rejectFilesNotAccept () {
        return this.$notification.warn({
          message: 'Warning',
          description: 'Only .xls .xlsx .csv files Accepted'
        })
      },
      // function executed when teacher remove the file uploaded
      removeFile () {
        this.studentsInfo = []
        this.studentsInfoHasError = false
        this.tableData = []
        return true
      },
      // function used to import file
      importFile (file) {
        const extension = ['xls', 'xlsx'].includes(file.name.split('.')[1])
        if (!extension) {
          this.$message.warning('Please upload Excel file')
          return false
        }

        const reader = new FileReader()
        const _this = this
        reader.onload = function (e) {
          const wb = XLSX.read(e.target.result, { type: 'binary' })

          // wb.SheetNames[0] is to get the name of the first sheet
          // wb.Sheets[Sheet's name] is to get the data of the first sheet
          const info = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]])

          // scan and filter the column
          let hasError = false
          _this.studentsInfo = []
          info.forEach(user => {
            const fieldNames = Object.keys(user)
            const newUser = {}
            let rowHasError = false
            _this.studentListColumns.forEach(field => {
              const fieldName = fieldNames.find(name => name.toLowerCase().indexOf(field.keyword) > -1)
              if (!field.optional && fieldName === undefined) {
                hasError = rowHasError = true
              } else if (fieldName !== undefined) {
                const value = user[fieldName]
                hasError = hasError || !field.validator(value)
                rowHasError = rowHasError || !field.validator(value)
                newUser[field.dataIndex] = value
              }
            })
            newUser.rowHasError = rowHasError
            _this.studentsInfo.push(newUser)
          })
          _this.studentsInfoHasError = hasError
          _this.studentListPagination.total = _this.studentsInfo.length
          _this.previewStudentsInfo(1, _this.studentListPagination.pageSize)
        }
        reader.readAsBinaryString(file.originFileObj)
      },
      previewStudentsInfo (current, pageSize) {
        const info = [...this.studentsInfo]
        this.tableData = info.splice((current - 1) * pageSize, pageSize)
        this.studentListPagination = { ...this.studentListPagination, current, pageSize }
      },
      save () {
        // validate the form. if there are errors, then this function will return
        this.$refs.editCourseFormRef.validate(valid => {
          if (!valid) {
            return this.$notification.warn({
              message: 'Warning',
              description: 'Your form still contains errors, please check'
            })
          }

          const importStudentsData = {
            students: this.studentsInfo.filter(student => !student.rowHasError).map(student => {
              const profile = pick(student, ['email', 'student_id'])
              if (student.gpa) profile.gpa = student.gpa
              return {
                username: student.username,
                student_profile: profile
              }
            })
          }

          if (this.mode === 1) {
            editCourse(this.selectedCourse.id, { title: this.editCourseForm.title }).then(() => {
              this.$notification.success({
                message: 'Success',
                description: 'Edit course success'
              })
              this.$router.push({ name: 'CourseManagement' })
            }).catch(() => {
              this.$notification.error({
                message: 'Error',
                description: 'Failed to edit course!'
              })
            })
          } else if (this.mode === 2) {
            importStudentsData.course = this.selectedCourse.id
            importStudentsData.default_password = this.editCourseForm.default_password
            importStudents(importStudentsData).then(({ data: result }) => {
              console.log(result)
              this.$notification.success({
                message: 'Success',
                description: `Successfully import ${result.added_students_count} students`
              })
              this.$router.push({ name: 'CourseManagement' })
            }).catch(() => {
              this.$notification.error({
                 message: 'Error',
                 description: 'Failed to import students!'
              })
            })
          } else {
            createCourse({ title: this.editCourseForm.title }).then(({ data: course }) => {
              importStudentsData.course = course.id
              importStudentsData.default_password = this.editCourseForm.default_password
              importStudents(importStudentsData).then(({ data: result }) => {
                this.$notification.success({
                  message: 'Success',
                  description: `Successfully create the course and import ${result.added_students_count} students`
                })
              }).catch(() => {
                this.$notification.warn({
                  message: 'Warning',
                  description: `Successfully create the course, but failed to import students`
                })
              })
              this.$store.dispatch('SetSelectedCourse', course)
              this.$router.push({ name: 'CourseManagement' })
            }).catch(() => {
              this.$notification.error({
                message: 'Error',
                description: 'Failed to create course!'
              })
            })
          }
        })
      }
    }
  }
</script>

<style scoped>

</style>
