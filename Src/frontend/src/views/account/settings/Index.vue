<template>
  <div class="page-header-index-wide">
    <a-card :bodyStyle="{ height: '100%' }" :style="{ height: '100%' }">
      <div class="account-settings-info-title">
        <span>Account Settings</span>
      </div>

      <a-row :gutter="16">
        <a-col :md="24" :lg="16">

          <a-form-model ref="form" layout="vertical" :model="form" :rules="rules">
            <a-form-model-item label="Old password" prop="old_password">
              <a-input v-model="form.old_password" type="password" />
            </a-form-model-item>
            <a-form-model-item label="New password" prop="new_password">
              <a-input v-model="form.new_password" type="password" />
            </a-form-model-item>

            <a-form-item>
              <a-button type="primary" @click="submit">Update</a-button>
            </a-form-item>
          </a-form-model>

        </a-col>
        <a-col :md="24" :lg="8" :style="{ minHeight: '180px' }">
          <div class="ant-upload-preview" @click="$refs.modal.edit(1)" >
            <a-icon type="cloud-upload-o" class="upload-icon"/>
            <div class="mask">
              <a-icon type="plus" />
            </div>
            <img :src="avatarMedium"/>
          </div>
        </a-col>

      </a-row>

    </a-card>

    <avatar-modal ref="modal" />
  </div>
</template>

<script>
  import { changePassword } from '@/api/users'
  import AvatarModal from './AvatarModal'
  import { mapGetters } from 'vuex'

  export default {
    name: 'Settings',
    components: {
      AvatarModal
    },
    data () {
      const validatePasswords = (rule, value, cb) => {
        if (this.form.old_password === '' && this.form.new_password === '' && value === '') {
          return cb()
        }
        if (value === '') {
          return cb(new Error('This field is required'))
        }
        cb()
      }
      return {
        form: {
          old_password: '',
          new_password: ''
        },
        rules: {
          old_password: [{
            validator: validatePasswords,
            trigger: 'blur'
          }],
          new_password: [{
            validator: validatePasswords,
            trigger: 'blur'
          }]
        }
      }
    },
    computed: mapGetters(['avatarMedium']),
    methods: {
      async submit () {
        const valid = await this.$refs.form.validate()
        if (valid) {
          changePassword(this.form).then(() => {
            this.$notification.success({
              message: 'Success',
              description: 'Change password successfully!'
            })
            this.$refs.form.resetFields()
          }).catch(err => {
            const data = err.response.data
            this.$notification.error({
              message: 'Error',
              description: (data && data.old_password) ? data.old_password[0] : 'Failed to change password!'
            })
          })
        }
      }
    }
  }
</script>

<style lang="less" scoped>
  .account-settings-info-title {
    color: rgba(0,0,0,.85);
    font-size: 20px;
    font-weight: 500;
    line-height: 28px;
    margin-bottom: 24px;
  }

  .avatar-upload-wrapper {
    height: 200px;
    width: 100%;
  }

  .ant-upload-preview {
    position: relative;
    margin: 0 auto;
    width: 100%;
    max-width: 180px;
    border-radius: 50%;
    box-shadow: 0 0 4px #ccc;

    .upload-icon {
      position: absolute;
      top: 0;
      right: 10px;
      font-size: 1.4rem;
      padding: 0.5rem;
      background: rgba(222, 221, 221, 0.7);
      border-radius: 50%;
      border: 1px solid rgba(0, 0, 0, 0.2);
    }

    .mask {
      opacity: 0;
      position: absolute;
      background: rgba(0, 0, 0, 0.4);
      cursor: pointer;
      transition: opacity 0.4s;

      &:hover {
        opacity: 1;
      }

      i {
        font-size: 2rem;
        position: absolute;
        top: 50%;
        left: 50%;
        margin-left: -1rem;
        margin-top: -1rem;
        color: #d6d6d6;
      }
    }

    img, .mask {
      width: 100%;
      max-width: 180px;
      height: 100%;
      border-radius: 50%;
      overflow: hidden;
    }
  }
</style>
