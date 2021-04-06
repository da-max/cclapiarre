<template>
  <header>
    <h1 class="uk-text-center">
      Liste des carousels
    </h1>
    <div class="uk-text-center uk-margin-large">
      <UtilsButton @click="showCarouselModal">
        Ajouter un carousel
      </UtilsButton>
    </div>
  </header>
</template>

<script>
import useCarousel from '@/composition/carousel/useCarousel'

import UtilsButton from '@/components/Utils/UtilsButton.vue'

export default {
    name: 'CarouselListHeader',
    components: {
        UtilsButton
    },
    setup () {
        const { showCarouselModal } = useCarousel()

        return {
            showCarouselModal
        }
    }
}
</script>
