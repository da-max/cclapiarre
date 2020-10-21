<template>
  <div id="app">
    <DefaultNavbar />
    <router-view/>
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