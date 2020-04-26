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
        <a-icon type="left"/>
        New Course
      </a-button>
      <!--Alert Area-->
      <a-alert style="margin-top: 20px" message="Reminder: Please click the course name for students management" type="info" showIcon />
      <!--The table of courses-->
      <a-table class="table-adjust" :columns="this.courseColumns" :dataSource="courseList" rowKey="id" :pagination="paginationAdjust">
        <template slot="name" slot-scope="text, record">
          <a @click="ShowManageStudentDialog(record)">{{ record.title }}</a>
        </template>
        <template slot="operation" slot-scope="text, record">
          <a-tooltip placement="top">
            <template slot="title">
              <span>Click to edit this course</span>
            </template>
            <a href="#" @click="EditCourseInfo(record)"><a-icon type="edit" />Edit</a>
          </a-tooltip>
          <a-tooltip>
            <template slot="title">
              <span>Click to delete this course</span>
            </template>
            <a class="a-adjust" href="#" style="font-color: red" @click="DeleteCourse(record)"><a-icon type="delete" />Delete</a>
          </a-tooltip>
        </template>
      </a-table>
    </a-card>
    <!--Student Mangement Modal-->
    <div>
      <a-modal title="Students Mangement" width="820px" v-model="studentManagementModalVisible">
        <a-form :model="studentManagementForm" :label-col="labelCol" :wrapper-col="wrapperCol">
          <!--Chosed course row-->
          <a-form-item label="Chosed course">
            <a-input v-model="studentManagementForm.choosedCourse" :disabled="true"/>
          </a-form-item>
          <!--student query and student list-->
        </a-form>
      </a-modal>
    </div>
  </div>
</template>

<script>
  import { getTeacherCourses } from '../../../api/teacher'
  import { mapGetters } from 'vuex'

  export default {
    name: 'CourseManagement',
    data () {
      return {
        // student management form layout settings
        labelCol: { span: 4 },
        wrapperCol: { span: 14 },
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
        // list used to store all the courses of current teacher
        courseList: [],
        // object used to adjust the pagination of the table
        paginationAdjust: {
          // default page size
          defaultPageSize: 10,
          // Show the number of total items
          showTotal: (total) => `Totally ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '12', '15', '25'],
          onShowSizeChange: (current, pageSize) => {
            this.pageSize = pageSize
            this.getCourses()
          },
          onChange: (page, pageSize) => {
            this.pageSize = pageSize
            this.pageNum = page
            this.getCourses()
          }
        },
        // variable used to control whether the student management modal is visible
        studentManagementModalVisible: false,
        // Form object used in the students management
        studentManagementForm: {
          choosedCourse: ''
        }
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
        getTeacherCourses().then(response => {
            this.courseList = response
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
      EditCourseInfo (x) {
        console.log(x)
      },
      DeleteCourse (x) {
        console.log(x)
      },
      // function used to show the student management dialog
      ShowManageStudentDialog (course) {
        this.studentManagementForm.choosedCourse = course.title
        this.studentManagementModalVisible = true
      }
    },
    created () {
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
</style>
