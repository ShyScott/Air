<template>
  <a-modal
    v-model="visible"
    title="Add a Student"
    width="800px"
    okText="Submit"
    cancelText="Cancel"
    :confirm-loading="submitLoading"
    @ok="submit"
    @cancel="close"
  >
    <div style="width: 640px">
      <a-form-model
        ref="form"
        v-bind="formLayout"
        :model="form"
        :rules="rules"
      >
        <!--Course name-->
        <a-form-model-item label="Course name">
          <a-input :value="selectedCourse === null ? '' : selectedCourse.title" disabled />
        </a-form-model-item>
        <!--Student name-->
        <a-form-model-item label="Student name" prop="username">
          <a-input v-model="form.username" />
        </a-form-model-item>
        <!--Student ID-->
        <a-form-model-item label="Student ID" prop="student_id">
          <a-input v-model="form.student_id" />
        </a-form-model-item>
        <!--Email-->
        <a-form-model-item label="Email" prop="email">
          <a-input v-model="form.email" />
        </a-form-model-item>
        <!--GPA-->
        <a-form-model-item label="GPA" prop="gpa">
          <a-input v-model="form.gpa" />
        </a-form-model-item>
        <!--default password-->
        <a-form-model-item label="Default Password" prop="default_password">
          <a-input v-model="form.default_password" />
        </a-form-model-item>
      </a-form-model>
    </div>
  </a-modal>
</template>

<script>
  import pick from 'lodash.pick'
  import { addStudentToTheCourse } from '@/api/teacher'
  import { mapGetters } from 'vuex'

  export default {
    name: 'AddStudentModal',
    data () {
      // GPA format validator
      const checkGPA = (rule, value, cb) => {
        if (value === '') return cb()
        const regFloat = /^\d+(.\d{1,2})?$/
        if (!regFloat.test(value)) {
          return cb(new Error('Please input a float number with no more than 2 decimal places'))
        }
        const gpa = parseFloat(value)
        if (gpa < 0 || gpa > 4) {
          return cb(new Error('Please input a valid GPA'))
        }
        return cb()
      }

      return {
        visible: false,
        form: {
          username: '',
          student_id: '',
          email: '',
          gpa: '',
          default_password: ''
        },
        // validation rules for the add student form
        rules: {
          // validation for username
          username: [
            { required: true, message: `Please input the student's name`, trigger: 'blur' },
            { pattern: /^[A-Za-z]+( +[A-Za-z]+)*$/, message: 'Please input a valid Student Name', trigger: 'blur' }
          ],
          student_id: [
            { required: true, message: `Please input the student's ID`, trigger: 'blur' }
          ],
          email: [
            { required: true, message: `Please input the student's Email Address`, trigger: 'blur' },
            { type: 'email', message: 'Please input a valid email address', trigger: 'blur' }
          ],
          gpa: [
            { validator: checkGPA, trigger: 'blur' }
          ],
          default_password: [
            { required: true, message: 'Please input the default password', trigger: 'blur' }
          ]
        },

        // layout settings for the add student form
        formLayout: {
          labelCol: { span: 8 },
          wrapperCol: { span: 16 }
        },

        // Loading status of submit button
        submitLoading: false
      }
    },
    computed: mapGetters(['selectedCourse']),
    methods: {
      show () {
        this.visible = true
      },
      close () {
        this.$refs.form.resetFields()
        this.visible = false
      },
      submit () {
        this.$refs.form.validate(valid => {
          // if all the info user input has past the validation
          if (valid) {
            this.submitLoading = true
            const { form } = this
            const profile = pick(form, ['student_id', 'email', 'gpa'])
            if (form.gpa === '') delete profile.gpa
            const parameter = {
              students: [{
                username: form.username,
                student_profile: profile
              }],
              course: this.selectedCourse.id,
              default_password: form.default_password
            }
            addStudentToTheCourse(parameter).then(() => {
              this.$emit('ok')
              this.close()
              return this.$notification.success({
                message: 'Message',
                description: 'Add new student Successful'
              })
            }).catch(error => {
              console.info(error)
              return this.$notification.error({
                message: 'Message',
                description: 'Add new student Failed'
              })
            }).finally(() => { this.submitLoading = false })
          } else {
            return this.$notification.warn({
              message: 'Message',
              description: 'Please provide valid information for submit'
            })
          }
        })
      }
    }
  }
</script>
