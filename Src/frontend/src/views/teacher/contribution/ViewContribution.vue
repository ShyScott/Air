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
          <a-icon type="like"/>
          <span>View Contribution</span>
        </a-breadcrumb-item>
      </a-breadcrumb>
      <div style="margin-top: 30px">
        <a-row>
          <a-col :span="16">
            <!--search & select bar-->
            <a-select
              show-search
              placeholder="Select a course. Input the course name to filter."
              style="width: 400px"
              :filterOption="false"
              @search="handleSearch"
              @change="handleChange"
            >
              <a-select-option v-for="(item, i) in courseList" :value="item.id" :key="i">
                {{ item.title }}
              </a-select-option>
            </a-select>
          </a-col>
          <a-col :offset="21">
            <a-button :disabled="contributionList.length === 0" @click="exportToExcel" type="primary"><a-icon type="export" />Export</a-button>
          </a-col>
        </a-row>
      </div>
      <!--table area-->
      <a-table
        id="outTable"
        size="middle"
        style="margin-top: 20px"
        :dataSource="contributionListPreview"
        :columns="contributionListColumns"
        :pagination="pagination"
        rowKey="student_id"
        @change="handleTableChange"
      />
    </a-card>
  </div>
</template>

<script>

  import { exportContribution, getTeacherCourses } from '@/api/teacher'
  import XLSX from 'xlsx'

  export default {
    name: 'ViewContribution',
    data () {
      return {
        // variable used to store the course info
        courseList: [],
        // course has been selected currently
        selectedCourseId: null,
        // list for contributions
        contributionList: [],
        // list for previewing contributions
        contributionListPreview: [],
        // pagination settings for contribution list
        pagination: {
          current: 1,
          pageSize: 10,
          total: 0,
          showTotal: (total) => `Total ${ total } items`,
          showSizeChanger: true,
          pageSizeOptions: ['10', '12', '15', '20']
        },
        // columns settings for the contribution list
        contributionListColumns: [
          {
            title: 'Student Name',
            dataIndex: 'username',
            width: '25%',
            align: 'center'
          },
          {
            title: 'Student ID',
            dataIndex: 'student_id',
            width: '25%',
            align: 'center'
          },
          {
            title: 'Contribution',
            dataIndex: 'contribution',
            width: '25%',
            align: 'center',
            customRender: text => (parseFloat(text) * 100).toFixed(2) + '%'
          },
          {
            title: 'Bonus',
            dataIndex: 'bonus',
            width: '25%',
            align: 'center'
          }
        ]
      }
    },
    methods: {
      // function used to move to main page
      moveToIndex () {
        this.$router.push('mainpage')
      },
      // get all courses
      getCourses () {
        getTeacherCourses().then(({ data: response }) => {
          this.courseList = response.results
        }).catch(error => {
          console.info(error)
          this.$notification.error({
            message: 'Error',
            description: 'Failed to get the information of available courses'
          })
        })
      },
      // executed when teacher wants to search
      handleSearch (value) {
        const parameter = { title: value }
        getTeacherCourses(parameter).then(({ data: response }) => {
          this.courseList = response.results
        }).catch(error => {
          console.info(error.response)
          this.$notification.error({
            message: 'Error',
            description: 'Failed to search the target course'
          })
        })
      },
      // function executed when different course is selected
      handleChange (value) {
        // console.log(value)
        this.selectedCourseId = value
        this.getContribution()
      },
      // get all the contributions of current course
      getContribution () {
        exportContribution(this.selectedCourseId).then(({ data: response }) => {
          this.contributionList = response
          this.pagination.total = response.length
          this.handleTableChange({ current: 1 })
        }).catch(error => {
          var errorInfo = 'Failed to get contribution information'
          if (error.response) {
            if (error.response.data) {
              errorInfo = error.response.data[0]
              this.$notification.warn({
                message: 'Warning',
                description: errorInfo
              })
            } else {
              this.$notification.error({
                message: 'Error',
                description: errorInfo
              })
            }
          }
        })
      },
      handleTableChange (pagination) {
        pagination = {
          ...this.pagination,
          ...pagination
        }
        this.pagination = pagination
        const data = [...this.contributionList]
        this.contributionListPreview = data.splice((pagination.current - 1) * pagination.pageSize, pagination.pageSize)
      },
      // function used to export the contribution info to excel file
      exportToExcel () {
        const courseName = this.courseList.find(item => item.id === this.selectedCourseId).title
        const data = [
          ['Student Name', 'Student ID', 'Contribution', 'Bonus'],
          ...this.contributionList.map(item => [item.username, item.student_id, item.contribution, item.bonus])
        ]
        const wb = XLSX.utils.book_new()
        const ws = XLSX.utils.aoa_to_sheet(data)
        XLSX.utils.book_append_sheet(wb, ws, courseName)
        XLSX.writeFile(wb, courseName + '.xlsx')
      }
    },
    created () {
      // get all the course info before page rendering
      this.getCourses()
    }
  }
</script>

<style scoped>

</style>
