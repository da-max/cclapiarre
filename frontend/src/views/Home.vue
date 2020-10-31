<template>
  <main>
    <Carousels v-if="response.loading === false" :carousels="response.data.allCarousels"></Carousels>
    <div
      uk-grid
      class="uk-margin-auto uk-width-4-5@xl uk-width-expands uk-position-relative"
    >
      <div class="uk-width-2-3@l uk-width-auto">Article</div>
      <div class="uk-width-1-3@l uk-width-auto uk-text-justify uk-padding">
        <PresentationCard></PresentationCard>
      </div>
    </div>
  </main>
</template>

<script>
import PresentationCard from '@/components/Home/PresentationCard'
import Carousels from '@/components/Home/Carousels'
import { useSetupTitle } from '@/composition/utils'
import { useDataFetcher } from '@/composition/useDataFetcher'

import CarouselAll from '@/graphql/Carousel/CarouselAll.gql'

export default {
  setup (props) {
    useSetupTitle('Accueil')
    const { error, response } = useDataFetcher({ query: CarouselAll })
    return {
      error,
      response
    }
  },
  components: {
    Carousels,
    PresentationCard
  }
}
</script>
