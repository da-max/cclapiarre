<template>
  <div id="app">
    <Loader v-if="loading" />
    <DefaultNavbar />
    <div class="uk-width-2-5@l uk-width4-5@s uk-margin-auto">
      <Alerts />
    </div>
    <router-view uk-height-viewport="offset-top: true; offset-bottom: true" />
    <DefaultFooter />
  </div>
</template>

<script>
import DefaultNavbar from '@/components/Utils/DefaultNavbar'
import DefaultFooter from '@/components/Utils/DefaultFooter'
import Loader from '@/components/Utils/Loader'
import Alerts from '@/components/Utils/Alert/Alerts'
import { mapState } from 'vuex'

export default {
  components: {
    DefaultNavbar,
    DefaultFooter,
    Alerts,
    Loader
  },
  beforeCreate () {
    this.$store.dispatch('auth/loadUser')
  },
  computed: {
    ...mapState(['loading'])
  }
}
</script>
