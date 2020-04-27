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
      <a-button class="addButton-adjust" type="primary" size="default">
        <a-icon type="coffee"/>
        New Course
      </a-button>
      <!--Alert Area-->
      <a-alert style="margin-top: 20px" message="Reminder: Please click the course name for students management" type="info" showIcon />
      <!--The table of courses-->
      <a-table class="table-adjust" :columns="this.courseColumns" :dataSource="courseList" rowKey="id" :pagination="paginationForCourseTable">
        <template slot="name" slot-scope="text, record">
          <a @click="DisplayInfoOnStudentManageCard(record)">{{ record.title }}</a>
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
          <!--tooltip for operation button-->
          <a-tooltip>
            <template slot="title">
              <span>Click to delete this course</span>
            </template>
            <a class="a-adjust" href="#" style="font-color: red" @click="DeleteCourse(record)"><a-icon type="delete" />Delete</a>
          </a-tooltip>
        </template>
      </a-table>
    </a-card>
    <!--Student management card area-->
    <a-card title="Course Info" style="margin-top: 20px">
      Chosed Course: {{ this.studentManagementForm.chosedCourse }}
      <div style="margin-bottom: 20px">
        <a-button class="addButton-adjust" type="primary" size="default" style="margin-right: 20px">
          <a-icon type="user-add"/>
          Add a Student
        </a-button>
        <a-button class="addButton-adjust" type="primary" size="default">
          <a-icon type="file-done"/>
          Import students from a file
        </a-button>
      </div>
      <a-table :columns="studentListColumns" :dataSource="studentList" rowKey="id" :pagination="paginationForStudentListTable">
        <!--Add delete button to operation slot-->
        <template slot="operation" slot-scope="text, record">
          <!--Operation Area-->
          <a-tooltip>
            <template slot="title">
              <span>Click to delete the student from this course</span>
            </template>
            <a class="a-adjust" href="#" style="font-color: red" @click="DeleteCourse(record)"><a-icon type="delete" />Delete</a>
          </a-tooltip>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script>
  import { getTeacherCourses, getCourseInfoById, getStudentListOfTheCourse } from '../../../api/teacher'
  import { mapGetters } from 'vuex'

  export default {
    name: 'CourseManagement',
    data () {
      return {
        // Used to indicate the header of the course table
        courseColumns: [{
          // Course name column
          title: 'Course Name',
          dataIndex: 'title',
          width: '30%',
          scopedSlots: { customRender: 'name' }
        },
          {
            // Duration column
            title: 'Duration',
            dataIndex: 'duration',
            width: '25%',
            scopedSlots: { customRender: 'duration' }
          },
          {
            // Student number column
            title: 'Number',
            dataIndex: 'students_count',
            width: '25%',
            scopedSlots: { customRender: 'students_count' }
          },
          {
            // operation column
            title: 'Operation',
            dataIndex: 'operation',
            width: '20%',
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
            scopedSlots: { cunstomRender: 'username' }
          },
          {
            // Email column
            title: 'Email Address',
            dataIndex: 'student_profile.email',
            width: '20%',
            scopedSlots: { customRender: 'email' }
          },
          {
            // Student ID column
            title: 'Student ID',
            dataIndex: 'student_profile.student_id',
            width: '20%',
            scopedSlots: { customRender: 'id' }
          },
          {
            // GPA column
            title: 'GPA',
            dataIndex: 'student_profile.gpa',
            width: '20%',
            scopedSlots: { customRender: 'gpa' }
          },
          {
            // operation column
            title: 'Operation',
            dataIndex: 'operation',
            width: '20%',
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
            this.getStudentList(this.selectedCourseId)
          },
          onChange: (page, pageSize) => {
            this.pagesizeForStudentList = pageSize
            this.pagenumForStudentList = page
            this.getStudentList(this.selectedCourseId)
          }
        },
        // Form object used in the students management
        studentManagementForm: {
          chosedCourse: ''
        },
        // variable used to control whether the course info edit modal is visible
        courseInfoEditModalVisible: false,
        // Form object used in the course info edit
        courseInfoEditForm: {
          id: 0,
          title: '',
          duration: '',
          students_count: '',
          form_method: 0,
          member_count_primary: 0,
          team_count_primary: 0,
          member_count_secondary: 0,
          team_count_secondary: 0,
          floating_band: 0
        },
        // The query info input by the user
        searchText: '',
        searchInput: null,
        searchedColumn: '',
        // the id of the course selected by user
        selectedCourseId: '',
        // pagination parameters for the course table
        totalForCourse: 0,
        pagenumForCourse: 1,
        pagesizeForCourse: 5,
        // pagination parameters for the student list table
        totalForStudentList: 0,
        pagenumForStudentList: 1,
        pagesizeForStudentList: 5
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
        getTeacherCourses(this.pagenumForCourse, this.pagesizeForCourse).then(response => {
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
          this.courseInfoEditForm = response
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
        getStudentListOfTheCourse(courseId, this.pagenumForStudentList, this.pagesizeForStudentList).then(response => {
          this.studentList = response.results
          // pagination settings
          this.totalForStudentList = response.count
          this.paginationForStudentListTable.total = response.count
          // console.log(this.studentList)
        })
      },
      DeleteCourse (x) {
        console.log(x)
      },
      // function used to fill the infomation supposed to be displayed in the Student Managemet Card
      // course is the info of course selected
      DisplayInfoOnStudentManageCard (course) {
        this.studentManagementForm.chosedCourse = course.title
        // console.log(course.id)
        this.selectedCourseId = course.id
        this.getStudentList(this.selectedCourseId)
      },
      // function used to show the course info edit modal
      moveToCourseInfoEditPage (course) {
        console.log(course.id)
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
