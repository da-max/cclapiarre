<template>
  <div v-if="images.length === 1">
    <img
      :src="'/media/' + images[0].image"
      :alt="images[0].alt"
      uk-img
      class="uk-box-shadow-medium"
    >
  </div>
  <UtilsSlider
    v-else
    base-url="/media/"
    :images="images"
  />
</template>

<script>
import { computed } from '@vue/composition-api'
import store from '@/store/index'
import UtilsSlider from '@/components/Utils/UtilsSlider'

export default {
    name: 'OrderHeaderImage',
    components: {
        UtilsSlider
    },
    setup () {
        const images = computed(() => store.getters['application/applicationImage'])
        return {
            images
        }
    }
}
</script>
