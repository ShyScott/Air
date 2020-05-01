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
        <a-table></a-table>
      </div>
    </a-card>
  </div>
</template>

<script>
  import { getTeacherCourses } from '../../../api/teacher'
  export default {
    name: 'TeamManagement',
    data () {
      return {
        // variable used to store all the courses
        courseList: []
        // columns for the team info table
      }
    },
    methods: {
      // function used to move to main page
      moveToIndex () {
        this.$router.push('mainpage')
      },
      // function used to get all the courses
      getCourses () {
        getTeacherCourses().then(({ data: response }) => {
          this.courseList = response.results
          // console.log(this.courseList)
        }).catch(error => {
          console.info(error)
          this.$notification.error({
            message: 'Error',
            description: 'Failed to get the information of available courses'
          })
        })
      }
    },
    created () {
      this.getCourses()
    }
  }
</script>

<style scoped>

</style>
