<template>
  <div>
    <template>
      <!--This is the area for the rendering of course cards-->
      <div style="background-color: #f1f2f5;">
        <a-card class="card-border" style="margin-bottom: 25px;">
          <a-row>
            <a-col>
              <!--Breadcrumb Area-->
              <a-breadcrumb class="breadcrumb-adjust">
                <a-breadcrumb-item href="">
                  <a-icon type="home" />
                </a-breadcrumb-item>
                <a-breadcrumb-item href="">
                  <a-icon type="user" />
                  <span>Application List</span>
                </a-breadcrumb-item>
                <a-breadcrumb-item>
                  Application
                </a-breadcrumb-item>
              </a-breadcrumb>
            </a-col>
          </a-row>
          <a-row>
            <a-col>
              <!--WelcomeArea-->
              <p style="font-size: 60px; margin-left: 20px; margin-bottom: 15px">
                <a-icon type="smile" style="font-size: 60px" />
                Welcome {{ this.nickname }}</p>
            </a-col>
          </a-row>
        </a-card>
        <a-card title="Your Courses" class="card-border">
          <a href="#" slot="extra" @click="moveToCoursePage">More</a>
          <a-row :gutter="16">
            <!--Each row 3 items, at most 6 items rendered-->
            <a-col :span="8" v-for="(item, i) in courseList" :key="item.id" v-if="i < 6">
              <a-card hoverable style="width: 100%; margin-bottom: 10px">
                <!--Course Card Image-->
                <img
                  alt="example"
                  src="https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
                  slot="cover"
                />
                <a-card-meta :title="item.title" description="This is the description">
                  <a-avatar
                    slot="avatar"
                    src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
                  />
                </a-card-meta>
              </a-card>
            </a-col>
          </a-row>
        </a-card>
      </div>
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
          this.courseList = response
          }
        ).catch(error => {
          console.info(error)
          this.$notification.error({
            message: 'Error',
            description: 'Failed to get the information of available courses'
        })
        })
      },
      // function used to move to the detailed page of course
      moveToCoursePage () {
        this.$router.push('course')
      }
    }
  }
</script>

<style lang="less" scoped>
  .card-border {
    border: 0px;
  }
  .breadcrumb-adjust {
    margin-bottom: 35px;
  }
</style>
