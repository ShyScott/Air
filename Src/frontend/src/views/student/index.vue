<template>
  <div>
    Index
    {{ this.nickname }}
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'
  export default {
    name: 'Index',
    computed: {
      ...mapGetters([
        'nickname'
      ])
    }
  }
</script>

<style scoped>

</style>
