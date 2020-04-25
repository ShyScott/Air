<script src="../../api/auth.js"></script>
<template>
  <div>
    Index
    {{ this.nickname }}
    {{ this.isTeacher }}
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'
  export default {
    name: 'Index',
    computed: {
      ...mapGetters([
        'nickname',
        'isTeacher'
      ])
    }
  }
</script>

<style scoped>

</style>
