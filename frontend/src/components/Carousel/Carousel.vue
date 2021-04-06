<template>
  <article class="uk-article">
    <h1 class="uk-article-title">
      {{ carousel.title }}
    </h1>
    <p class="uk-article-meta">
      Position du carousel : {{ carousel.position }}
    </p>
    <p class="uk-article-meta">
      Lien de l’image :
      <a
        target="_blank"
        :href="'/media/' + carousel.image"
      >{{ carousel.image }}</a>
    </p>
    <div class="uk-flex uk-flex-around uk-margin-medium">
      <p v-html="carousel.description" />
      <img
        :src="'/media/' + carousel.image"
        uk-img
        width="40%"
        alt="Image pour le carousel"
      >
    </div>
    <div
      v-if="actions"
      class="uk-flex uk-flex-center"
    >
      <div>
        <UtilsButton
          v-show="canChangeCarousel"
          @click="showCarouselModal(carousel.id)"
        >
          Modifier
        </UtilsButton>
        <UtilsButton
          v-show="canDeleteCarousel"
          class="uk-margin-medium-left"
          type="danger"
          @click="showDeleteCarouselModal(carousel.id)"
        >
          Supprimer
        </UtilsButton>
      </div>
    </div>
  </article>
</template>

<script>
import useCarousel from '@/composition/carousel/useCarousel'

import UtilsButton from '@/components/Utils/UtilsButton'

export default {
    name: 'Carousel',
    components: {
        UtilsButton
    },
    props: {
        actions: {
            default: false,
            required: false,
            type: Boolean
        },
        carousel: {
            required: true,
            type: Object
        }
    },
    setup () {
        const {
            canChangeCarousel,
            canDeleteCarousel,
            showCarouselModal,
            showDeleteCarouselModal
        } = useCarousel()

        return {
            canChangeCarousel,
            canDeleteCarousel,
            showCarouselModal,
            showDeleteCarouselModal
        }
    }
}
</script>
