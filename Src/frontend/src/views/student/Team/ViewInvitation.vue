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
          <a-icon @click="moveToTeamManagementPage" type="team"/>
          <span @click="moveToTeamManagementPage">Team Management</span>
        </a-breadcrumb-item>
        <a-breadcrumb-item href="">
          <a-icon type="star"/>
          <span>View Invitation</span>
        </a-breadcrumb-item>
      </a-breadcrumb>
      <!--Select Area-->
      <div style="margin-top: 40px">
        <span style="margin-right: 15px"> Course Name: </span>
        <a-select
          placeholder="Please select the course"
          style="width: 400px"
          show-search
          :filterOption="false"
          @search="handleSearch"
          @change="handleChange"
        >
          <a-icon slot="suffixIcon" type="smile" />
        </a-select>
      </div>
    </a-card>
  </div>
</template>

<script>
  export default {
    name: 'ViewInvitation',
    data () {
      return {
      }
    },
    methods: {
      // function used to move to main page
      moveToIndex () {
        this.$router.push({ name: 'Index' })
      },
      // function used to move to the team management page
      moveToTeamManagementPage () {
        this.$router.push('/team')
      },
      // TODO: function used to search the target course
      handleSearch (value) {
      },
      // TODO:function executed when user select the target course
      handleChange () {
      }
    },
    created () {
    }
  }
</script>

<style scoped>

</style>
