<template>
  <UtilsModal id="carousel-delete-modal">
    <template #header>
      Supprimer le carousel ?
    </template>
    <template #body>
      <p>
        Vous êtes sur le point de supprimer le carousel {{ carousel.title }},
        <span class="uk-text-danger">attention, cette action est irréversible.</span>
      </p>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          type="secondary"
          class="uk-modal-close uk-margin-medium-right"
        >
          Annuler
        </UtilsButton>
        <UtilsButton
          type="danger"
          @click="removeCarousel"
        >
          Supprimer
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import useCarousel from '@/composition/carousel/useCarousel'

import UtilsButton from '@/components/Utils/UtilsButton'
import UtilsModal from '@/components/Utils/UtilsModal'

export default {
    name: 'CarouselDeleteModal',
    components: {
        UtilsButton,
        UtilsModal
    },
    setup () {
        const { carousel, deleteCarousel, closeDeleteCarouselModal } = useCarousel()

        const removeCarousel = () => {
            deleteCarousel()
            closeDeleteCarouselModal()
        }

        return { carousel, removeCarousel }
    }
}
</script>
