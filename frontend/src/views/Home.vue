<template>
  <main>
    <Carousels :carousels='allCarousels'></Carousels>
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

<script>
import PresentationCard from '@/components/Home/PresentationCard'
import Carousels from '@/components/Home/Carousels'
import gql from 'graphql-tag'

export default {
  components: {
    Carousels,
    PresentationCard
  },
  data () {
    return {
      allCarousels: []
    }
  },
  apollo: {
    allCarousels: gql`query {
      allCarousels {
        id,
        title,
        position,
        description,
        image
      }
    }`
  }
}
</script>
