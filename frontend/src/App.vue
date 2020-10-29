<template>
  <div id="app">
    <DefaultNavbar />
    <Alerts />
    <router-view uk-height-viewport="offset-top: true; offset-bottom: true" />
    <DefaultFooter />
  </div>
</template>

<script>
import DefaultNavbar from '@/components/Utils/DefaultNavbar'
import DefaultFooter from '@/components/Utils/DefaultFooter'
import Alerts from '@/components/Utils/Alert/Alerts'

export default {
  components: {
    DefaultNavbar,
    DefaultFooter,
    Alerts
  },
  mounted () {
    this.$store.dispatch('auth/loadUser')
  }
}
</script>
