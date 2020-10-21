<template>
  <div id="app">
    <DefaultNavbar />
    <router-view uk-height-viewport="offset-top: true; offset-top: true" />
    <DefaultFooter />
  </div>
</template>

<script>
import DefaultNavbar from '@/components/Utils/DefaultNavbar'
import DefaultFooter from '@/components/Utils/DefaultFooter'
export default {
  components: {
    DefaultNavbar,
    DefaultFooter
  }
}
</script>
