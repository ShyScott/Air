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
              placeholder="Select a course"
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
            <a-button :disabled="contributionList === null" @click="exportToExcel" type="primary"><a-icon type="export" />Export</a-button>
          </a-col>
        </a-row>
      </div>
      <!--table area-->
      <a-table
        id="outTable"
        style="margin-top: 20px"
        :dataSource="contributionList"
        :columns="contributionListColumns"
        :pagination="pagination"
        rowKey="student_id"
      >
      </a-table>
    </a-card>
  </div>
</template>

<script>

  import { exportContribution, getTeacherCourses } from '../../../api/teacher'
  import FileSaver from 'file-saver'
  import XLSX from 'xlsx'

  export default {
    name: 'ViewContribution',
    data () {
      return {
        // variable used to store the course info
        courseList: [],
        // course has been selected currently
        selectedCourseId: '',
        // list for contributions
        contributionList: null,
        // pagination settings for contribution list
        pagination: {
          disabled: true,
          defaultPageSize: 150,
          total: 0,
          showTotal: (total) => `Total ${ total } items`,
          hideOnSinglePage: true
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
            align: 'center'
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
          // console.log(this.contributionList)
        }).catch(error => {
          var errorInfo = 'Failed to get contribution information'
          if (error.response) {
            if (error.response.data) {
              errorInfo = error.response.data[0]
              console.info(error.response)
              this.$notification.warn({
                message: 'Warning',
                description: errorInfo
              })
            } else {
              console.info(error.response)
              this.$notification.error({
                message: 'Error',
                description: errorInfo
              })
            }
          }
        })
      },
      // function used to export the contribution info to excel file
      exportToExcel () {
        // when transforming to excel, use original format
        var xlsxParam = { raw: true }
        var wb = XLSX.utils.table_to_book(document.querySelector('#outTable'), xlsxParam)
        var wbout = XLSX.write(wb, {
          bookType: 'xlsx',
          bookSST: true,
          type: 'array'
        })
        try {
          var courses = this.courseList
          courses = courses.filter((item) => {
            return item.id === this.selectedCourseId
          })
          const fileName = courses[0].title + '.xlsx'
          FileSaver.saveAs(
            new Blob(
              [wbout],
              { type: 'application/octet-stream;charset=utf-8' }),
            fileName
          )
        } catch (e) {
          if (typeof console !== 'undefined') console.log(e, wbout)
        }
        return wbout
      }
    }
  }
</script>

<style scoped>

</style>
