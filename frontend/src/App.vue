<template>
  <div>
    <DefaultNavbar></DefaultNavbar>
    <router-view />
    <DefaultFooter></DefaultFooter>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component'
import DefaultFooter from '@/components/Utils/DefaultFooter.vue'
import DefaultNavbar from '@/components/Utils/DefaultNavbar.vue'

@Options({
  components: {
    DefaultFooter,
    DefaultNavbar
  }
})
export default class App extends Vue {}
</script>
