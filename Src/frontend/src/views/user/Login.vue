<template>
  <div class="main">
    <a-form
      id="formLogin"
      class="user-layout-login"
      ref="formLogin"
      :form="form"
      @submit="handleSubmit"
    >
      <a-alert v-if="isLoginError" type="error" showIcon style="margin-bottom: 24px;" message="Wrong username or password!" />
      <a-form-item>
        <a-input
          size="large"
          type="text"
          placeholder="Username"
          v-decorator="[
            'username',
            {rules: [{ required: true, message: 'Please input your username' }], validateTrigger: 'change'}
          ]"
        >
          <a-icon slot="prefix" type="user" :style="{ color: 'rgba(0,0,0,.25)' }"/>
        </a-input>
      </a-form-item>

      <a-form-item>
        <a-input
          size="large"
          type="password"
          autocomplete="false"
          placeholder="Password"
          v-decorator="[
            'password',
            {rules: [{ required: true, message: 'Please input your password' }], validateTrigger: 'blur'}
          ]"
        >
          <a-icon slot="prefix" type="lock" :style="{ color: 'rgba(0,0,0,.25)' }"/>
        </a-input>
      </a-form-item>

      <a-form-item>
        <a-checkbox v-decorator="['rememberMe', { valuePropName: 'checked' }]">Remember me</a-checkbox>
      </a-form-item>

      <a-form-item style="margin-top:24px">
        <a-button
          size="large"
          type="primary"
          htmlType="submit"
          class="login-button"
          :loading="loginBtn"
          :disabled="loginBtn"
        >Login</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
// import md5 from 'md5'
import { mapActions } from 'vuex'

export default {
  data () {
    return {
      isLoginError: false,
      form: this.$form.createForm(this),
      csrfToken: '',
      loginBtn: true
    }
  },
  methods: {
    ...mapActions(['Login', 'Logout']),
    handleSubmit (e) {
      e.preventDefault()
      const {
        form: { validateFields },
        Login
      } = this

      this.loginBtn = true

      const validateFieldsKey = ['username', 'password']

      validateFields(validateFieldsKey, { force: true }, (err, values) => {
        if (!err) {
          values.csrfmiddlewaretoken = this.csrfToken
          Login(values)
            .then((res) => this.loginSuccess(res))
            .catch(err => this.requestFailed(err))
            .finally(() => {
              this.loginBtn = false
            })
        } else {
          setTimeout(() => {
            this.loginBtn = false
          }, 600)
        }
      })
    },
    loginSuccess () {
      this.$router.push({ path: '/' })
      this.isLoginError = false
    },
    requestFailed () {
      this.isLoginError = true
    }
  },
  mounted () {
    const failedToGetToken = () => {
      this.$notification.error({
        message: 'Error',
        description: 'Failed to retrieve critical information from back-end for login process. Please contact admin.'
      })
      console.warn('Warning: failed to get CSRF token')
    }

    // get the first csrf token from backend
    this.axios({
      method: 'get',
      baseURL: '/api-auth',
      url: '/login/'
    }).then(response => {
      const tokenReg = /csrfmiddlewaretoken['"].+value=['"](.+)['"]/
      const token = response.data.match(tokenReg)
      if (token) {
        this.csrfToken = token[1]
        this.loginBtn = false
      } else {
        failedToGetToken()
      }
    }).catch(() => {
      failedToGetToken()
    })
  }
}
</script>

<style lang="less" scoped>
.user-layout-login {
  label {
    font-size: 14px;
  }

  button.login-button {
    padding: 0 15px;
    font-size: 16px;
    height: 40px;
    width: 100%;
  }
}
</style>
