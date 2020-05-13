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

      <a-button class="addButton-adjust" type="primary" size="default" @click="addCourse">
        <a-icon type="coffee"/>
        New Course
      </a-button>

      <!--Alert Area-->
      <a-alert style="margin-top: 20px" message="Reminder: Please click the course name for students management" type="info" showIcon />

      <!--The table of courses-->
      <a-spin :spinning="courseLoading">
        <a-table class="table-adjust" :columns="this.courseColumns" :dataSource="courseList" rowKey="id" :pagination="coursePagination">
          <template slot="name" slot-scope="text, record">
            <a @click="selectCourse(record)">{{ record.title }}</a>
            <span v-if="record.is_confirmed === true"><a-icon style="color: red; margin-left: 10px" type="lock"></a-icon></span>
            <span v-else><a-icon style="color: #daa520; margin-left: 10px" type="unlock"></a-icon></span>
          </template>

          <!--operation area of the table-->
          <template slot="operation" slot-scope="text, record">
            <!--tooltip for operation button-->
            <a-tooltip title="Click to edit this course">
              <a @click="editCourse(record)"><a-icon type="edit" />Edit</a>
            </a-tooltip>
            <a-popconfirm title="Are you sure to delete this course?" @confirm="ConfirmCourseDelete(record.id)">
              <!--tooltip for operation button-->
              <a-tooltip title="Click to delete this course">
                <a class="a-adjust"><a-icon type="delete" />Delete</a>
              </a-tooltip>
            </a-popconfirm>
          </template>
        </a-table>
      </a-spin>
    </a-card>

    <!--Student management card area-->
    <a-card
      v-if="selectedCourse !== null"
      style="margin-top: 20px"
      :title="`Student Management - ${selectedCourse.title}`"
    >

      <a-input-search
        enterButton
        style="margin: 10px 0; width: 50%"
        v-model="searchStudent"
        placeholder="Search student by username or student id"
        :loading="searchStudentLoading"
        @search="getStudents(true)"
      />

      <div style="margin-bottom: 20px">
        <a-button
          class="addButton-adjust"
          type="primary"
          style="margin-right: 20px"
          :disabled="selectedCourse.is_confirmed"
          @click="addStudent"
        >
          <a-icon type="user-add"/>Add a Student
        </a-button>
        <a-button
          class="addButton-adjust"
          type="primary"
          @click="importStudentsFromFile"
          :disabled="selectedCourse.is_confirmed"
        >
          <a-icon type="file-done"/>Import students from a file
        </a-button>
      </div>

      <a-spin :spinning="studentLoading">
        <a-table :columns="studentColumns" :dataSource="studentList" rowKey="id" :pagination="studentPagination">
          <!--Add delete button to operation slot-->
          <template slot="operation" slot-scope="text, record">
            <!--Operation Area-->
            <a-popconfirm
              title="Are you sure to remove this student from the course?"
              @confirm="ConfirmStudentRemove(selectedCourse.id, record.id)"
            >
              <a-tooltip title="Click to delete the student from this course">
                <a class="a-adjust"><a-icon type="delete" />Remove</a>
              </a-tooltip>
            </a-popconfirm>
          </template>
        </a-table>
      </a-spin>
    </a-card>

    <add-student-modal ref="addStudentModal" @ok="handleAddStudentOk"/>
  </div>
</template>

<script>
  import { getTeacherCourses, getStudentListOfTheCourse, deleteCourse, removeStudent } from '@/api/teacher'
  import AddStudentModal from './modal/AddStudentModal'
  import { mapGetters } from 'vuex'

  export default {
    name: 'CourseManagement',
    components: {
      AddStudentModal
    },
    data () {
      return {
        // Loading state of course table
        courseLoading: false,
        // Used to indicate the header of the course table
        courseColumns: [
          {
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
        courseList: [],
        // object used to adjust the pagination of the course table
        coursePagination: {
          current: 1,
          pageSize: 5,
          // Show the number of total items
          showTotal: (total) => `Total ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '12', '15', '25'],
          onShowSizeChange: (current, pageSize) => {
            this.coursePagination.current = current
            this.coursePagination.pageSize = pageSize
            this.getCourses()
          },
          onChange: (current, pageSize) => {
            this.coursePagination.pageSize = pageSize
            this.coursePagination.current = current
            this.getCourses()
          }
        },

        // Loading state for student table
        studentLoading: false,
        // Columns settings for the student list table in the student management card
        studentColumns: [
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
        // list used to store all the students taking the course selected
        studentList: [],
        // object used to adjust the pagination of the student list table
        studentPagination: {
          current: 1,
          pageSize: 5,
          // Show the number of total items
          showTotal: (total) => `Total ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '15', '20', '25'],
          onShowSizeChange: (current, pageSize) => {
            this.studentPagination.current = current
            this.studentPagination.pageSize = pageSize
            this.getStudents()
          },
          onChange: (current, pageSize) => {
            this.studentPagination.pageSize = pageSize
            this.studentPagination.current = current
            this.getStudents()
          }
        },

        // The query info input by the user
        searchStudent: '',
        searchStudentLoading: false
      }
    },
    computed: mapGetters(['selectedCourse']),
    methods: {
      // function used to move to main page
      moveToIndex () {
        this.$router.push('mainpage')
      },
      // function used to get all the courses available of current Teacher
      getCourses () {
        this.courseLoading = true
        const parameter = { page: this.coursePagination.current, size: this.coursePagination.pageSize }
        getTeacherCourses(parameter).then(({ data: response }) => {
          // console.log(response)
          this.courseList = response.results
          // pagination settings
          this.coursePagination.total = response.count
          }
        ).catch(error => {
          console.info(error)
          this.$notification.error({
            message: 'Error',
            description: 'Failed to get the information of available courses'
          })
        }).finally(() => { this.courseLoading = false })
      },
      // function used to fill the information supposed to be displayed in the Student Management Card
      // course is the info of course selected
      selectCourse (course) {
        this.$store.dispatch('SetSelectedCourse', course)
        this.searchStudent = ''
        this.getStudents()
      },
      // function used to route to the add course page
      addCourse () {
        this.$store.dispatch('SetEditCourseMode', 3)
        const target = { name: 'EditCourse' }
        this.$router.push(target)
      },
      // function used to show the course info edit modal
      editCourse (course) {
        this.$store.dispatch('SetEditCourseMode', 1)
        this.$store.dispatch('SetSelectedCourse', course)
        const target = { name: 'EditCourse' }
        this.$router.push(target)
      },
      // function executed when user confirm to delete the course
      ConfirmCourseDelete (courseId) {
        // console.log(courseId)
        deleteCourse(courseId).then(() => {
          // solve the problem: if there is only 1 student left in the current page, delete this course will lead to a 404 since that current page is not existed anymore
          if (this.coursePagination.total % this.coursePagination.pageSize === 1) {
            this.coursePagination.current -= 1
          }
          // re-render
          this.getCourses()
          // this.getStudents(this.selectedCourseId)
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
        })
      },

      // get the students list according to the course id given
      getStudents (isSearch = false) {
        this.studentLoading = true
        if (isSearch) {
          this.studentPagination.current = 1
          this.searchStudentLoading = true
        }
        // process data
        const parameter = {
          course: this.selectedCourse.id,
          page: this.studentPagination.current,
          size: this.studentPagination.pageSize
        }
        // check if the query content is empty
        if (this.searchStudent !== '') parameter.search = this.searchStudent
        getStudentListOfTheCourse(parameter).then(({ data: response }) => {
          this.studentList = response.results
          // pagination settings
          this.studentPagination.total = response.count
        }).catch(error => {
          console.info(error)
          this.$notification.error({
            message: 'Error',
            description: 'Failed to get the information of students'
          })
        }).finally(() => { this.studentLoading = this.searchStudentLoading = false })
      },
      // function used to show the Add student modal
      addStudent () {
        this.$refs.addStudentModal.show()
      },
      importStudentsFromFile () {
        this.$store.dispatch('SetEditCourseMode', 2)
        const route = { name: 'EditCourse' }
        this.$router.push(route)
      },
      // function executed when user confirm to remove the student from the course
      ConfirmStudentRemove (courseId, studentId) {
        // console.log(courseId)
        // console.log(studentId)
        removeStudent(courseId, studentId).then(() => {
          // solve the problem: if there is only 1 student left in the current page, remove this student will lead to a 404 since that current page is not existed anymore
          const { studentPagination: pagination } = this
          if (pagination.total % pagination.pageSize === 1) {
            pagination.current -= 1
          }
          // re-render 2 tables
          this.getCourses()
          this.getStudents()
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
        })
      },
      // function executed when user click the submit button of the add student modal
      handleAddStudentOk () {
        // refresh the two tables
        this.getCourses()
        this.getStudents()
      }
    },
    created () {
      // get all the courses belonging to the current teacher after initialization
      this.getCourses()
      // get all students if has selected courses
      if (this.selectedCourse !== null) this.getStudents()
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
    color: #EE2C2C;
    &:not(:first-child) {
      margin-left: 20px;
    }
  }

  .highlight {
    background-color: rgb(255, 192, 105);
    padding: 0px;
  }
</style>
