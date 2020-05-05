<template>
  <div>
    <a-card>
      <a-row>
        <a-col :span="7">
          <div style="justify-content: center; display: flex; margin-top: 100px; margin-bottom: 60px; flex-direction: column; align-items: center">
            <!--Avatar area-->
            <a-row>
              <a-avatar :size="240" src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png" />
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
          <a-card style="margin-top: 30px" title="Your Courses" class="card-border">
            <a href="#" slot="extra" @click="showMoreCourseModal">More</a>
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
          <!--TimeLine Area-->
          <a-card class="card-border" title="Operation Log">
            <template>
              <div style="margin-top: 35px">
                <a-row>
                  <a-col :span="12">
                    <div style="margin-top: 35px; justify-content: center; display: flex; font-size: 32px">
                      <a-button size="large" type="link">View All Operation Records<a-icon type="container" /></a-button>
                    </div>
                  </a-col>
                  <a-col :span="12">
                    <a-timeline pending="Recording..." :reverse="false">
                      <a-timeline-item>Create a services site 2015-09-01</a-timeline-item>
                      <a-timeline-item>Solve initial network problems 2015-09-01</a-timeline-item>
                      <a-timeline-item>Technical testing 2015-09-01</a-timeline-item>
                    </a-timeline>
                  </a-col>
                </a-row>
              </div>
            </template>
          </a-card>
        </a-col>
      </a-row>
    </a-card>
    <!--Show more course info modal-->
    <template>
      <div>
        <a-modal v-model="showMoreCourseModalVisible" title="All Course Information" width="800px">
          <template slot="footer">
            <a-button key="back" type="primary" @click="handleMoreCourseModalCancel">
              Return
            </a-button>
          </template>
          <a-table :dataSource="this.courseList" rowKey="id" :columns="courseTableColumns" :pagination="courseListPagination">
          </a-table>
        </a-modal>
      </div>
    </template>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'
  import { getStudentCourses } from '../../api/student'

  export default {
    name: 'Index',
    data () {
      return {
        // variable used to store the courses of current student
        courseList: [],
        // variable used to control whether to display the more courses info modal
        showMoreCourseModalVisible: false,
        // columns for the course info table
        courseTableColumns: [
            {
              // Course name
              title: 'Course Name',
              dataIndex: 'title',
              width: '30%',
              scopedSlots: { customRender: 'coursename' }
            },
            {
              // Duration column
              title: 'Duration',
              dataIndex: 'duration',
              width: '40%',
              scopedSlots: { customRender: 'duration' }
            },
            {
              // Student number column
              title: 'Student Number',
              dataIndex: 'students_count',
              width: '30%',
              scopedSlots: { customRender: 'students_count' }
            }
        ],
        // pagination settings for course list table
        courseListPagination: {
          // default page size
          defaultPageSize: 5,
          // Show the number of total items
          showTotal: (total) => `Total ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '15', '20', '25'],
          onShowSizeChange: (current, pageSize) => {
            this.pageNumForCourse = current
            this.pageSizeForCourse = pageSize
            this.getCourses()
          },
          onChange: (page, pageSize) => {
            this.pageSizeForCourse = pageSize
            this.pageNumForCourse = page
            this.getCourses()
          }
        },
        // current page num for courses
        pageNumForCourse: 1,
        // current page size for submission
        pageSizeForCourse: 5
      }
    },
    methods: {
      // function used to get the courses info of the current student
      getCourses () {
        getStudentCourses().then(({ data: response }) => {
          this.courseList = response.results
          this.courseListPagination.total = response.count
          this.formatDuration()
        }).catch(error => {
          if (error.response) {
            return this.$notification.error({
              message: 'Error',
              description: 'Failed to get available course information'
            })
          }
        })
      },
      // function used to transfer the duration to proposed format
      formatDuration () {
        for (let i = 0; i < this.courseList.length; i++) {
          let durationAfterFormat = ''
          const durationBeforeTransfer = this.courseList[i].duration
          const durationSplit = durationBeforeTransfer.split('-')
          // console.log(durationSplit)
          // process the data split
          // 1st Semester - 9 - 1
          if (durationSplit[1] >= 9 || durationSplit[1] <= 1) {
            durationAfterFormat = durationSplit[0] + '-' + (durationSplit[0] + 1) + ' Semester 1'
          } else {
            durationAfterFormat = (durationSplit[0] - 1) + '-' + durationSplit[0] + ' Semester 2'
          }
          this.courseList[i].duration = durationAfterFormat
          // console.log(this.courseList[i].duration)
        }
      },
      // function used to control whether the more course info modal should be display or not
      showMoreCourseModal () {
        this.showMoreCourseModalVisible = true
      },
      // function used when user click return button in the more course info modal
      handleMoreCourseModalCancel () {
        this.showMoreCourseModalVisible = false
      }
    },
    computed: {
      ...mapGetters([
        'nickname',
        'isTeacher'
      ])
    },
    created () {
      this.getCourses()
    }
  }
</script>

<style scoped>
  .card-border {
    border: 0px;
  }
</style>
