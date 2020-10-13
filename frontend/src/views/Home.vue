<template>
  <main>
    Carousel

    <div
      uk-grid
      class="uk-margin-auto uk-width-4-5@xl uk-width-expands uk-position-relative"
    >
      <div class="uk-width-2-3@l uk-width-auto">
        Article
      </div>
      <div class="uk-width-1-3@l uk-width-auto uk-text-justify uk-padding">
        <PresentationCard></PresentationCard>
      </div>
    </div>
  </main>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component'
import PresentationCard from '@/components/Home/PresentationCard.vue' // @ is an alias to /src

@Options({
  components: {
    PresentationCard
  }
})
export default class Home extends Vue {}
</script>
