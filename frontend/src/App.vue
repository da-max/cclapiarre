<template>
  <div id="app">
    <div class="uk-background-secondary uk-padding-small uk-text-center uk-text-danger uk-text-bold">
      Attention, vous êtes actuellement sur la version bêta de Cclapiarre. Les données que vous rentrez sur ce site ne seront pas accéssible sur le site <a href="http://cclapiarre.deblan.fr">cclapiarre.deblan.fr</a> !!
    </div>
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
    computed: {
        ...mapState(['loading'])
    },
    beforeCreate () {
        this.$store.dispatch('auth/loadUser')
        this.$store.dispatch('application/getApplications')
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

.required-label:after {
  content: "*";
  margin-left: 0.4rem;
  color: rgb(240, 86, 115);
}
</style>
