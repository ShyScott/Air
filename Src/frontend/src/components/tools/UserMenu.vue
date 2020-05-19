<template>
  <div class="user-wrapper">
    <div class="content-box">
      <a-dropdown>
        <span class="action ant-dropdown-link user-dropdown-menu">
          <a-avatar class="avatar" :src="avatar">{{ nickname[0].toUpperCase() }}</a-avatar>
          <span>{{ nickname }}</span>
        </span>
        <a-menu slot="overlay" class="user-dropdown-menu-wrapper">
          <a-menu-item>
            <router-link :to="{ name: 'Settings' }">
              <a-icon type="setting"/>
              <span>Account Settings</span>
            </router-link>
          </a-menu-item>
          <a-menu-divider/>
          <a-menu-item>
            <a href="javascript:;" @click="handleLogout">
              <a-icon type="logout"/>
              <span>Logout</span>
            </a>
          </a-menu-item>
        </a-menu>
      </a-dropdown>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'UserMenu',
  computed: {
    ...mapGetters(['nickname', 'avatar'])
  },
  methods: {
    ...mapActions(['Logout']),
    handleLogout () {
      this.$confirm({
        title: 'Confirmation',
        content: 'Are you really want to logout?',
        onOk: () => {
          return this.Logout({}).then(() => {
            setTimeout(() => {
              window.location.reload()
            }, 16)
          }).catch(err => {
            this.$message.error({
              title: 'Error',
              description: err.message
            })
          })
        },
        onCancel () {
        }
      })
    }
  }
}
</script>
