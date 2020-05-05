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
      <!--view invitations button-->
      <div style="margin-top: 50px; margin-right: 30px; display: flex; justify-content: flex-end; flex-direction: column; align-items: flex-end">
        <a-button type="primary"><a-icon type="star" /> View Invitations</a-button>
      </div>
      <!--Table area-->
      <div style="margin-top: 25px">
        <a-table></a-table>
      </div>
    </a-card>
  </div>
</template>

<script>
  export default {
    name: 'TeamManagement',
    data () {
      return {
      }
    },
    methods: {
      // function used to move to main page
      moveToIndex () {
        this.$router.push('mainpage')
      },
      // function used to get the course info of current student
      getCourses () {
      }
    },
    created () {
    }
  }
</script>

<style scoped>
  .border-adjust {
    border: 0px;
  }
</style>
