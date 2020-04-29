<template>
  <div>
    <a-card>
      <!--Tabs Area-->
      <template>
        <a-form-model :model="addCourseForm" :rules="addCourseFormRules" ref="addCourseFormRef" :label-col="labelCol" :wrapper-col="wrapperCol">
          <a-tabs defaultActiveKey="1">
            <!--Tab 1 used to register common course information-->
            <a-tab-pane key="1">
              <span slot="tab">
                <a-icon type="idcard" />
                Course Info
              </span>
              <!--Course name-->
              <a-form-item label="Course Name" style="width: 850px; margin-top: 20px">
                <a-input v-model="addCourseForm.course_name"></a-input>
              </a-form-item>
              <!--duration given by the system-->
              <a-form-item label="Duration" style="width: 850px">
                <a-input v-model="addCourseForm.duration" :disabled="true"></a-input>
              </a-form-item>
            </a-tab-pane>
            <!-- Tab 2 used to import student list by file-->
            <a-tab-pane key="2">
              <span slot="tab">
                <a-icon type="usergroup-add" />
                Import Students
              </span>
              <a-row>
                <a-col>
                  <!--Alert Area-->
                  <a-alert style="margin-top: 20px" message="Reminder: Please upload your 'Student_List.xlsx' in the area below" type="info" showIcon />
                </a-col>
              </a-row>
              <a-row>
                <a-col style="width: 150%">
                  <a-form-item style="margin-top: 20px">
                    <template>
                      <a-upload-dragger
                        name="file"
                        :multiple="false"
                        :directory="false"
                        accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel"
                        action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
                        :beforeUpload="checkIfFileExisted"
                        :remove="removeFile"
                        @change="handleChange"
                        @reject="rejectFilesNotAccept"
                      >
                        <p class="ant-upload-drag-icon">
                          <a-icon type="inbox" />
                        </p>
                        <p class="ant-upload-text">Click or drag file to this area to upload</p>
                        <p class="ant-upload-hint">
                          Support for a single or bulk upload. Strictly prohibit from uploading company data or other band files
                        </p>
                      </a-upload-dragger>
                    </template>
                  </a-form-item>
                </a-col>
              </a-row>
            </a-tab-pane>
          </a-tabs>
        </a-form-model>
      </template>
    </a-card>

  </div>
</template>

<script>
  import XLSX from 'xlsx'
  export default {
    name: 'AddCourse',
    data () {
      return {
        // form layout settings
        labelCol: { span: 4 },
        wrapperCol: { span: 16 },
        // form object used to add a new course
        addCourseForm: {
          course_name: '',
          duration: ''
        },
        // validation rules for course add
        addCourseFormRules: {},
        // get current time
        currentTime: new Date(),
        // Year of the duration
        durationY: '',
        // Semester of the duration
        durationS: '',
        // Excel file upload
        // if we need to transfer the file stream to binary - false
        rABS: false,
        wb: '',
        tableData: []
      }
    },
    created () {
      // get the current local time for duration transformation
      var _this = this
      // if the first semester
      if (new Date().getMonth() >= 7 || new Date().getMonth() <= 1) {
        // console.log('sem 1')
        _this.durationS = 'Semester 1'
        _this.durationY = new Date().getFullYear() + ' - ' + new Date().getFullYear() + 1
        // console.log(_this.durationY)
      } else {
        // if the second semester
        // console.log('sem 2')
        _this.durationS = 'Semester 2'
        _this.durationY = new Date().getFullYear() - 1 + ' - ' + new Date().getFullYear()
        // console.log(_this.durationY)
      }
      // Merge the duration
      _this.addCourseForm.duration = _this.durationY + ' ' + _this.durationS
      // console.log(_this.addCourseForm.duration)
    },
    methods: {
      // file upload change handler
      handleChange (info) {
        const status = info.file.status
        if (status !== 'uploading') {
          // console.log(info, info.fileList)
        }
        // if file uploading done
        if (status === 'done') {
          // if succeed
          this.$notification.success({
            message: 'Success',
            description: `${info.file.name} is uploaded successfully`
          })
          // import the file content
          this.importf(info.file)
        } else if (status === 'error') {
          // if failing
          this.$notification.error({
            message: 'Error',
            description: `${info.file.name} file upload failed.`
          })
        }
      },
      // function used to reject files that not accept
      rejectFilesNotAccept () {
        return this.$notification.warn({
          message: 'Warning',
          description: 'Only .xls .xlsx .csv files Accepted'
        })
      },
      // Teacher can only upload at most one excel file
      checkIfFileExisted (file) {
        return new Promise((resolve, reject) => {
          // if file is already uploaded
          if (this.tableData.length !== 0) {
            this.$notification.error({
              message: 'Error',
              description: 'You can only upload one file'
            })
            // reject the file
            // eslint-disable-next-line prefer-promise-reject-errors
            return reject(false)
          } else {
            return resolve(true)
          }
        })
      },
      // function executed when teacher remove the file uploaded
      removeFile () {
        return new Promise((resolve, reject) => {
          // reset the variable tableData
          this.tableData = []
          return resolve(true)
        })
      },
      // function used to import file
      importf (file) {
        var _this = this
        this.file = file
        const extention = file.name.split('.')[1] === 'xls'
        const extention2 = file.name.split('.')[1] === 'xlsx'
        // console.log(extention,extention2,isLt5M)
        if (!extention && !extention2) {
          this.$message.warning('Please upload Excel file')
          return false
        }
        // const data1 = XLSX.utils.sheet_to_json(file.name)

        var f = file.originFileObj
        var that = this
        var reader = new FileReader()
        reader.onload = function (e) {
          // console.log(e)
          let wb = that.wb
          var data = e.target.result
          if (that.rABS) {
            wb = XLSX.read(btoa(that.fixdata(data)), {
              // transfer
              type: 'base64'
            })
          } else {
            wb = XLSX.read(data, {
              type: 'binary'
            })
          }
          // wb.SheetNames[0] is to get the name of the first sheet
          // wb.Sheets[Sheet's name] is to get the data of the first sheet
          // document.getElementById("demo").innerHTML= JSON.stringify( XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]) );
          _this.tableData = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]])
          // _this.tableData = data1
          // console.log(_this.tableData)
        }
        if (this.rABS) {
          reader.readAsArrayBuffer(f)
        } else {
          reader.readAsBinaryString(f)
        }
      },
      fixdata (data) {
        // file stream transferred to binary string
        var o = ''
        var l = 0
        var w = 10240
        for (; l < data.byteLength / w; ++l) o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w, l * w + w)))
        o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w)))
        return o
      }
    }
  }
</script>

<style scoped>

</style>
