<template>
  <section>
    <p
      v-if="carousels.length === 0"
      class="uk-text-center"
    >
      Aucun carousel.
    </p>
    <div
      v-else
      class="uk-width-1-2@m uk-margin-auto"
    >
      <carousel
        v-for="carousel in carousels"
        :key="carousel.id"
        :carousel="carousel"
        :actions="true"
        class="uk-padding uk-background-default"
      />
    </div>
    <CarouselModal />
    <CarouselDeleteModal />
  </section>
</template>

<script>
import useCarousel from '@/composition/carousel/useCarousel'
import Carousel from '@/components/Carousel/Carousel'
import CarouselModal from '@/components/Carousel/CarouselList/CarouselModal'
import CarouselDeleteModal from '@/components/Carousel/CarouselList/CarouselDeleteModal'

export default {
    name: 'CarouselListSection',
    components: {
        Carousel,
        CarouselModal,
        CarouselDeleteModal
    },
    setup () {
        const { carousels } = useCarousel()

        return {
            carousels
        }
    }
}
</script>
