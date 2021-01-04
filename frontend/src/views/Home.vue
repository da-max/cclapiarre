<template>
  <main>
    <Carousels
      v-if="!loading"
      :carousels="result.allCarousels"
    />
    <div
      uk-grid
      class="uk-margin-auto uk-width-4-5@xl uk-width-expands uk-position-relative"
    >
      <div class="uk-width-2-5@l uk-width4-5@s uk-margin-auto">
        <Alerts />
      </div>
      <div class="uk-width-2-3@l uk-width-auto">
        Article
      </div>
      <div class="uk-width-1-3@l uk-width-auto uk-text-justify uk-padding">
        <PresentationCard />
      </div>
    </div>
  </main>
</template>

<script>
import PresentationCard from '@/components/Home/PresentationCard'
import Alerts from '@/components/Utils/Alert/Alerts'
import Carousels from '@/components/Home/Carousels'
import { useSetupTitle } from '@/composition/useUtils'
import { useQuery } from '@vue/apollo-composable'
import CarouselAll from '@/graphql/Carousel/CarouselAll.gql'

export default {
  components: {
    Carousels,
    PresentationCard,
    Alerts
  },
  setup (props) {
    useSetupTitle('Accueil')
    const { result, loading } = useQuery(CarouselAll)
    return {
      result,
      loading
    }
  }
}
</script>
