<template>
  <div>
    <template>
      <a-card title="Your Courses">
        <a href="#" slot="extra">more</a>
        <a-card-grid style="width:50%;text-align:center">Content</a-card-grid>
        <a-card-grid style="width:50%;text-align:center">Content</a-card-grid>
        <a-card-grid style="width:50%;text-align:center">Content</a-card-grid>
        <a-card-grid style="width:50%;text-align:center">Content</a-card-grid>
      </a-card>
    </template>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'
  import { getTeacherCourses } from '../../api/teacher'
  export default {
    name: 'Index',
    data () {
      return {
        courseList: []
      }
    },
    computed: {
      ...mapGetters([
        'nickname'
      ])
    },
    created () {
      this.getCourses()
    },
    methods: {
      // function used to get all the courses available of current Teacher
      getCourses () {
        getTeacherCourses().then(response => {
          // eslint-disable-next-line eqeqeq
          if (response.code != 200) {
            return this.$notification.open({
              message: 'Error',
              description: 'Failed to get the information of available courses',
              icon: <a-icon type="frown" style="color: #B22222" />
            })
          }
          this.courseList = response.data
          console.log(this.courseList)
          }
        )
      }
    }
  }
</script>

<style scoped>

</style>
