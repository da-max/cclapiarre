<template>
  <div id="app">
    <Loader v-if="loading" />
    <DefaultNavbar />
    <router-view uk-height-viewport="offset-top: true; offset-bottom: true" />
    <DefaultFooter />
  </div>
</template>

<script>
import DefaultNavbar from '@/components/Utils/DefaultNavbar'
import DefaultFooter from '@/components/Utils/DefaultFooter'
import Loader from '@/components/Utils/Loader'
import { mapState } from 'vuex'

export default {
  components: {
    DefaultNavbar,
    DefaultFooter,
    Loader
  },
  beforeCreate () {
    this.$store.dispatch('auth/loadUser')
    this.$store.dispatch('application/getApplications')
  },
  computed: {
    ...mapState(['loading'])
  }
}
</script>

<style lang="scss">
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
