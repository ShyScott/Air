<template>

  <a-modal
    title="Change Avatar"
    :visible="visible"
    :maskClosable="false"
    :confirmLoading="confirmLoading"
    :width="800"
    :footer="null"
    @cancel="close">
    <a-row>
      <a-col :xs="24" :md="12" :style="{height: '350px'}">
        <vue-cropper
          ref="cropper"
          :img="options.img"
          :info="true"
          :centerBox="options.centerBox"
          :autoCrop="options.autoCrop"
          :autoCropWidth="options.autoCropWidth"
          :autoCropHeight="options.autoCropHeight"
          :fixedBox="options.fixedBox"
          @realTime="realTime"
        >
        </vue-cropper>
      </a-col>
      <a-col :xs="24" :md="12" :style="{height: '350px'}">
        <div class="avatar-upload-preview">
          <img :src="previews.url" :style="previews.img"/>
        </div>
      </a-col>
    </a-row>
    <br>
    <a-row>
      <a-col :xs="24" :md="12">
        <div style="display: flex; justify-content: space-between">
          <a-upload name="file" :beforeUpload="beforeUpload" :showUploadList="false">
            <a-button icon="upload">Select image</a-button>
          </a-upload>
          <a-button icon="plus" @click="changeScale(1)"/>
          <a-button icon="minus" @click="changeScale(-1)"/>
          <a-button icon="undo" @click="rotateLeft"/>
          <a-button icon="redo" @click="rotateRight"/>
        </div>
      </a-col>
      <a-col :xs="24" :md="12">
        <div style="display: flex; justify-content: space-evenly">
          <a-button type="primary" @click="submit(false)">Save</a-button>
          <a-button type="danger" @click="submit(true)">Delete current avatar</a-button>
        </div>
      </a-col>
    </a-row>
  </a-modal>

</template>
<script>
import { changeAvatar } from '@/api/users'
import { mapGetters } from 'vuex'

export default {
  data () {
    return {
      visible: false,
      confirmLoading: false,
      fileObj: null,
      options: {
        img: '',
        centerBox: true,
        autoCrop: true,
        autoCropWidth: 200,
        autoCropHeight: 200,
        fixedBox: true
      },
      previews: {}
    }
  },
  computed: mapGetters(['avatarMedium']),
  methods: {
    edit () {
      this.visible = true
      this.previews = {
        url: this.avatarMedium,
        img: {}
      }
    },
    close () {
      this.visible = false
    },
    changeScale (num) {
      num = num || 1
      this.$refs.cropper.changeScale(num)
    },
    rotateLeft () {
      this.$refs.cropper.rotateLeft()
    },
    rotateRight () {
      this.$refs.cropper.rotateRight()
    },
    beforeUpload (file) {
      this.fileObj = file
      const reader = new FileReader()
      // 把Array Buffer转化为blob 如果是base64不需要
      // 转化为base64
      reader.readAsDataURL(file)
      reader.onload = () => {
        this.options.img = reader.result
      }
      // 转化为blob
      // reader.readAsArrayBuffer(file)

      return false
    },

    // 上传图片（点击上传按钮）
    submit (isDelete) {
      if (!isDelete && this.fileObj === null) {
        return this.$notification.warn({
          message: 'Warning',
          description: 'Please select an image first!'
        })
      }

      const _this = this
      const onSuccess = () => {
        _this.$notification.success({
          message: 'Success',
          description: 'Update avatar successfully!'
        })
        // _this.$emit('ok', response.url)
        _this.close()
        // update user info
        _this.$store.dispatch('GetInfo')
      }
      const onFailure = () => {
        _this.$notification.error({
          message: 'Error',
          description: 'Failed to update avatar!'
        })
      }
      const onFinally = () => {
        _this.confirmLoading = false
      }

      this.confirmLoading = true
      const formData = new FormData()
      if (isDelete) {
        formData.append('avatar', '')
        changeAvatar(formData).then(onSuccess).catch(onFailure).finally(onFinally)
      } else {
        this.$refs.cropper.getCropBlob((data) => {
          formData.append('avatar', data, _this.fileObj.name)
          changeAvatar(formData).then(onSuccess).catch(onFailure).finally(onFinally)
        })
      }
    },

    realTime (data) {
      if (data.url !== '') this.previews = data
    }
  }
}
</script>

<style lang="less" scoped>

  .avatar-upload-preview {
    position: absolute;
    top: 50%;
    transform: translate(50%, -50%);
    width: 200px;
    height: 200px;
    border-radius: 50%;
    box-shadow: 0 0 4px #ccc;
    overflow: hidden;

    img {
      width: 100%;
      height: 100%;
    }
  }
</style>
