<template>
  <main>
    <Carousels v-if="!loading" :carousels="result.allCarousels"></Carousels>
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
import { useQuery } from '@vue/apollo-composable'
import CarouselAll from '@/graphql/Carousel/CarouselAll.gql'

export default {
  setup (props) {
    useSetupTitle('Accueil')
    const { result, loading } = useQuery(CarouselAll)
    return {
      result,
      loading
    }
  },
  components: {
    Carousels,
    PresentationCard
  }
}
</script>
