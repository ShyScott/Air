<template>
  <div>
    <template>
      <!--This is the area for the rendering of course cards-->
      <div style="background-color: #f1f2f5;">
        <a-card :bordered="false" style="margin-bottom: 25px; margin-top: 10px">
          <a-avatar :size="64" :src="avatar" />
          <span style="font-size: 48px; margin-bottom: 15px; vertical-align: middle">
            Welcome back, {{ nickname }}
          </span>
        </a-card>
        <a-card
          :bordered="false"
          style="margin-bottom: 25px"
          :bodyStyle="{ padding: '8px 0 0 0' }"
          title="Recent Courses"
        >
          <a slot="extra" @click="moveToCoursePage">More</a>
          <a-table :dataSource="courseList" :columns="columns" :pagination="false" rowKey="id" size="middle" />
        </a-card>
      </div>
    </template>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'
  import { getTeacherCourses } from '@/api/teacher'
  import { convertDuration } from '@/utils/util'
  import moment from 'moment'
  export default {
    name: 'Index',
    data () {
      return {
        courseList: [],
        columns: [
          {
            title: 'Course Name',
            dataIndex: 'title',
            align: 'center'
          },
          {
            title: 'Duration',
            dataIndex: 'duration',
            align: 'center'
          },
          {
            title: 'Students Count',
            dataIndex: 'students_count',
            align: 'center'
          }
        ]
      }
    },
    computed: {
      ...mapGetters([
        'nickname', 'avatar'
      ])
    },
    created () {
      this.getCourses()
    },
    methods: {
      // function used to get all the courses available of current Teacher
      getCourses () {
        // default: display 6 courses on the main page
        getTeacherCourses({ size: 8, ordering: '-duration' }).then(response => {
          this.courseList = response.data.results.map(course => {
            course.duration = convertDuration(moment(course.duration))
            return course
          })
          // console.log(this.courseList)
        }).catch(() => {
          this.$notification.error({
            message: 'Error',
            description: 'Failed to get the information of available courses'
          })
        })
      },
      // function used to move to the detailed page of course
      moveToCoursePage () {
        this.$router.push({ name: 'CourseManagement' })
      }
    }
  }
</script>

<style lang="less" scoped>
  .breadcrumb-adjust {
    margin-bottom: 35px;
  }
</style>
