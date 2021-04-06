<template>
  <UtilsModal
    id="carousel-modal"
    :center="true"
    :container="true"
    :esc-close="false"
  >
    <template #header>
      <h1 class="uk-modal-title">
        {{ carousel.id ? 'Modifier': 'Ajouter' }} un carousel
      </h1>
    </template>
    <template #body>
      <CarouselForm />
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          type="secondary"
          class="uk-modal-close"
        >
          Annuler
        </UtilsButton>
        <UtilsButton
          class="uk-margin-medium-left"
          type="primary"
          @click="saveCarousel"
        >
          {{ carousel.id ? 'Modifier': 'Ajouter' }}
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import useCarousel from '@/composition/carousel/useCarousel'

import CarouselForm from '@/components/Carousel/CarouselList/CarouselForm'
import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
    name: 'CarouselModal',
    components: {
        UtilsModal,
        UtilsButton,
        CarouselForm
    },
    setup () {
        const { carousel, saveCarousel } = useCarousel()

        return {
            carousel,
            saveCarousel
        }
    }

}
</script>
