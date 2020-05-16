<template>
  <div>
    <a-card :bodyStyle="{ padding: '0 12px' }">
      <a-row>
        <a-col :span="7">
          <div style="justify-content: center; display: flex; margin-top: 100px; margin-bottom: 60px; flex-direction: column; align-items: center">
            <!--Avatar area-->
            <a-row>
              <a-avatar :size="240" :src="avatarMedium" />
            </a-row>
            <!--Welcome Area-->
            <div style="margin-top: 55px">
              <a-row>
                <span style="font-size: 35px; text-align: center">Welcome back <a-icon type="smile" /></span>
                <br>
                <span style="text-align: center; display: flex; justify-content: center; font-size: 27px">Dear {{ this.nickname }}</span>
              </a-row>
            </div>
          </div>
        </a-col>
        <a-col :span="17">
          <a-card style="margin-top: 30px" title="Your Courses" :bordered="false">
            <a-table :dataSource="this.courseList" rowKey="id" :columns="courseTableColumns" :pagination="courseListPagination" />
          </a-card>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script>
  import moment from 'moment'
  import { mapGetters } from 'vuex'
  import { getStudentCourses } from '../../api/student'
  import { convertDuration } from '../../utils/util'

  export default {
    name: 'Index',
    data () {
      return {
        // variable used to store the courses of current student
        courseList: [],
        // columns for the course info table
        courseTableColumns: [
            {
              // Course name
              title: 'Course Name',
              dataIndex: 'title',
              align: 'center',
              width: '30%'
            },
            {
              // Duration column
              title: 'Duration',
              dataIndex: 'duration',
              align: 'center',
              width: '40%'
            },
            {
              // Student number column
              title: 'Students Count',
              dataIndex: 'students_count',
              align: 'center',
              width: '30%'
            }
        ],
        // pagination settings for course list table
        courseListPagination: {
          // Show the number of total items
          showTotal: (total) => `Total ${ total } items`,
          total: 0,
          current: 1,
          pageSize: 10,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '15', '20', '25'],
          onShowSizeChange: this.getTableCourses,
          onChange: this.getTableCourses
        }
      }
    },
    methods: {
      // function used to get the courses info of the current student for table
      getTableCourses (current, pageSize) {
        this.courseListPagination = {
          ...this.courseListPagination,
          current,
          pageSize
        }
        const parameter = { page: current, size: pageSize }
        getStudentCourses(parameter).then(({ data: response }) => {
          this.courseList = response.results.map(course => {
            course.duration = convertDuration(moment(course.duration))
            return course
          })
          this.courseListPagination.total = response.count
        }).catch(error => {
          if (error.response) {
            return this.$notification.error({
              message: 'Error',
              description: 'Failed to get available course information'
            })
          }
        })
      }
    },
    computed: {
      ...mapGetters([
        'nickname',
        'avatarMedium'
      ])
    },
    created () {
      this.getTableCourses(this.courseListPagination.current, this.courseListPagination.pageSize)
    }
  }
</script>

<style scoped>
  .card-border {
    border: 0px;
  }
</style>
