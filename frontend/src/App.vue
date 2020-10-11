<template>
  <main>
    <div id="nav">
      dadoiajdzaio
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view />
    <DefaultFooter></DefaultFooter>
  </main>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component'
import DefaultFooter from '@/components/Utils/DefaultFooter.vue'

@Options({
  components: {
    DefaultFooter
  }
})
export default class App extends Vue {}
</script>
