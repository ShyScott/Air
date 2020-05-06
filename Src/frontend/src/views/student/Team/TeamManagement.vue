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
      <!--Operation area-->
      <div style="margin-top: 45px">
        <a-row>
          <a-col :span="7">
            <!--search bar-->
            <a-input-search placeholder="Please input course name" v-model="queryContent" enter-button @search="onSearch" />
          </a-col>
          <a-col style="display: flex; justify-content: flex-end;" :span="17">
            <!--view invitations button-->
            <a-button type="primary"><a-icon type="star" /> View Invitations</a-button>
          </a-col>
        </a-row>
      </div>
      <!--Table area-->
      <div style="margin-top: 25px">
        <a-table :dataSource="this.courseList" :columns="this.teamTableColumns" rowKey="id" :pagination="this.paginationForTeamTable">
          <!--Team member column-->
          <template slot="teamMembers" slot-scope="text, record">
            <span v-if="record.team_in !== null">
              <span style="margin-right: 10px" v-for="item in record.team_in.members" :key="item.id">
                {{ item.username }}
              </span>
            </span>
          </template>
          <!--Operation column-->
          <template slot="operation" slot-scope="text, record">
            <!--case 1: The student has not been in any team in this course-->
            <span v-if="record.team_in === null">
              <!--tooltip for operation button-->
              <a-tooltip placement="top">
                <template slot="title">
                  <span>Click to create a new team</span>
                </template>
                <a href="#" @click="showCreateTeamModal(record)"><a-icon type="usergroup-add" />Create team</a>
              </a-tooltip>
            </span>
            <!--Case 2: The student has been in a team, and the team is confirmed-->
            <span v-else-if="record.is_confirmed === 'YES'">
              <!--tooltip for operation button-->
              <a-tooltip>
                <template slot="title">
                  <span>Click to vote a team leader for your team</span>
                </template>
                <a href="#" @click="showVoteTeamLeaderModal"><a-icon type="crown" />Vote leader</a>
              </a-tooltip>
            </span>
            <!--Case 3: The student already in a team, but the team not yet confirmed-->
            <span v-else>
              <a-tooltip>
                <template slot="title">
                  <span>Click to invite new member</span>
                </template>
                <a href="#" style="margin-right: 10px" @click="showInviteNewMember"><a-icon type="user-add" />Invite</a>
              </a-tooltip>
              <a-popconfirm title="Are you sure to exit this team?" @confirm="confirmExitCurrentTeam(record)" @cancel="cancelExitCurrentTeam">
                <!--tooltip for operation button-->
                <a-tooltip>
                  <template slot="title">
                    <span>Click to exit this team</span>
                  </template>
                  <a href="#" style="color: red"><a-icon type="api" />Exit team</a>
                </a-tooltip>
              </a-popconfirm>
            </span>
          </template>
        </a-table>
      </div>
    </a-card>
    <!--Create team modal-->
    <template>
      <div>
        <a-modal width="800px" v-model="createTeamModalVisible" title="Create New Team" on-ok="handleCreateNewTeamOk">
          <template slot="footer">
            <a-button key="cancel" @click="handleCreateNewTeamCancel">
              Return
            </a-button>
            <a-button key="submit" type="primary" @click="handleCreateNewTeamOk">
              Submit
            </a-button>
          </template>
          <!--Create new team modal-->
          <a-form-model
            :model="createNewTeamForm"
            :rules="createNewTeamFormRules"
            ref="createNewTeamFormRef"
            :label-col="labelCol"
            :wrapper-col="wrapperCol"
          >
            <a-form-model-item label="Team Name" prop="teamName">
              <a-input v-model="createNewTeamForm.teamName" allow-clear></a-input>
            </a-form-model-item>
          </a-form-model>
        </a-modal>
      </div>
    </template>
  </div>
</template>

<script>
  import { createNewTeam, getStudentCourses, queryCourse } from '../../../api/student'

  export default {
    name: 'TeamManagement',
    data () {
      return {
        // variable used to store course list
        courseList: [],
        // page num
        pageNum: 1,
        // page size
        pageSize: 5,
        // columns for the team table
        teamTableColumns: [
          {
            // Course title column
            title: 'Course Name',
            dataIndex: 'title',
            width: '15%',
            scopedSlots: { customRender: 'title' }
          },
          {
            // Team name column
            title: 'Team Name',
            dataIndex: 'team_in.name',
            width: '10%',
            scopedSlots: { customRender: 'teamName' }
          },
          {
            // Member list
            title: 'Team Members',
            dataIndex: 'team_in.members',
            width: '20%',
            scopedSlots: { customRender: 'teamMembers' }
          },
          {
            // whether is confirmed or not
            title: 'Confirmation Status',
            dataIndex: 'is_confirmed',
            width: '15%',
            scopedSlots: { customRender: 'confirmation_status' }
          },
          {
            // Duration
            title: 'Duration',
            dataIndex: 'duration',
            width: '20%',
            scopedSlots: { customRender: 'confirmation_status' }
          },
          {
            // operation
            title: 'Operation',
            dataIndex: 'operation',
            width: '20%',
            scopedSlots: { customRender: 'operation' }
          }
        ],
        // object used to adjust the pagination of the course table
        paginationForTeamTable: {
          // default page size
          defaultPageSize: 5,
          // Show the number of total items
          showTotal: (total) => `Totally ${ total } items`,
          total: 0,
          showSizeChanger: true,
          pageSizeOptions: ['5', '10', '12', '15', '25'],
          onShowSizeChange: (current, pageSize) => {
            this.pageNum = current
            this.pageSize = pageSize
            // if there is still content left in the search bar
            // execute the query function instead of getCourses()
            if (this.queryContent !== '') {
              // re-render
              return this.queryCourseByCourseName()
            }
            // re-render
            this.getCourses()
          },
          onChange: (page, pageSize) => {
            this.pageSize = pageSize
            this.pageNum = page
            // if there is still content left in the search bar
            // execute the query function instead of getCourses()
            if (this.queryContent !== '') {
              // re-render
              return this.queryCourseByCourseName()
            }
            // re-render
            this.getCourses()
          }
        },
        // variable used to control the display of create team modal
        createTeamModalVisible: false,
        // layout settings for the add submission form
        labelCol: { span: 5 },
        wrapperCol: { span: 16 },
        // form object for create new team form
        createNewTeamForm: {
          teamName: ''
        },
        // validation rules for create new team form
        createNewTeamFormRules: {
          teamName: [
            { required: true, message: 'Please input your team name', trigger: ['blur', 'change'] }
          ]
        },
        // variable used to store the id of course selected
        selectedCourseId: '',
        // query content input by the user
        queryContent: ''
      }
    },
    methods: {
      // function used to move to main page
      moveToIndex () {
        this.$router.push('mainpage')
      },
      // function used to get the course info of current student
      getCourses () {
        const parameter = { page: this.pageNum, size: this.pageSize }
        getStudentCourses(parameter).then(({ data: response }) => {
          this.courseList = response.results
          this.paginationForTeamTable.total = response.count
          this.processCourseList()
          // console.log(this.courseList)
        }).catch(error => {
          if (error.response) {
            console.info(error.response)
            return this.$notification.error({
              message: 'Error',
              description: 'Failed to get the information of available courses'
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
      // function used to process the data in the courseList
      processCourseList () {
        this.formatDuration()
        this.formatIsConfirmed()
      },
      // function used to format the confirmation status in the courselist
      formatIsConfirmed () {
        for (let i = 0; i < this.courseList.length; i++) {
          if (this.courseList[i].is_confirmed === true) {
            this.courseList[i].is_confirmed = 'YES'
          } else {
            this.courseList[i].is_confirmed = 'NO'
          }
        }
      },
      // function used to control the show of creat team modal
      // TODO
      showCreateTeamModal (course) {
        // store the selected course id
        this.selectedCourseId = course.id
        // console.log(this.selectedCourseId)
        this.createTeamModalVisible = true
      },
      // function used to control the show of vote team leader modal
      // TODO
      showVoteTeamLeaderModal () {
        console.log('Vote Team Leader')
      },
      // function executed when user confirm to quit the team
      // TODO
      confirmExitCurrentTeam () {
        console.log('Exit Team')
      },
      // function executed when user calcel to exit current team
      cancelExitCurrentTeam () {
        console.log('Cancel')
      },
      // function used to control the show of invite new member modal
      showInviteNewMember () {
        console.log('Invite')
      },
      // function executed when user click cancel button in the create new team modal
      handleCreateNewTeamCancel () {
        this.$refs.createNewTeamFormRef.resetFields()
        this.createTeamModalVisible = false
      },
      // function executed when user click submit button in the create new team modal
      handleCreateNewTeamOk () {
        // console.log('submit')
        this.submitNewTeam()
        this.$refs.createNewTeamFormRef.resetFields()
        this.getCourses()
        this.createTeamModalVisible = false
      },
      // function used to create a new team
      submitNewTeam () {
        const parameter = { name: this.createNewTeamForm.teamName, course: this.selectedCourseId }
        createNewTeam(parameter).then(({ data: response }) => {
          return this.$notification.success({
            message: 'Success',
            description: 'Create new team successful'
          })
        }).catch(error => {
          // if error occurs
          if (error.response) {
            console.info(error.response)
            return this.$notification.error({
              message: 'Error',
              description: 'Failed to create new team'
            })
          }
        })
      },
      // function used to query what user input
      queryCourseByCourseName () {
        const parameter = { title: this.queryContent, page: this.pageNum, size: this.pageSize }
        queryCourse(parameter).then(({ data: response }) => {
          this.courseList = response.results
          this.paginationForTeamTable.total = response.count
        })
      },
      // function executed when search button is clicked
      onSearch () {
        this.queryCourseByCourseName()
      }
    },
    created () {
      this.getCourses()
    }
  }
</script>

<style scoped>
  .border-adjust {
    border: 0px;
  }
</style>
