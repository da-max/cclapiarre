<template>
  <main>
    <CarouselListHeader class="uk-margin-large-top" />
    <AlertsStyling />
    <CarouselListSection />
  </main>
</template>

<script>
import useCarousel from '@/composition/carousel/useCarousel'

import AlertsStyling from '@/components/Utils/Alert/AlertsStyling'
import CarouselListHeader from '@/components/Carousel/CarouselList/CarouselListHeader'
import CarouselListSection from '@/components/Carousel/CarouselList/CarouselListSection'

export default {
    name: 'CarouselList',
    components: {
        AlertsStyling,
        CarouselListHeader,
        CarouselListSection
    },
    setup () {
        const { getCarousels } = useCarousel()

        getCarousels()
    }
}
</script>
