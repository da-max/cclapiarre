<template>
  <UtilsSlider
    base-url="/static/Images/Coffee/"
    :images="images"
  />
</template>

<script>
import { reactive, toRefs } from '@vue/composition-api'
import UtilsSlider from '@/components/Utils/UtilsSlider.vue'

export default {
  name: 'CoffeeOrderHeaderImage',
  components: { UtilsSlider },
  setup () {
    const state = reactive({
      images: [
        {
          image: 'coffee.jpg',
          alt: 'Image de présentation de l’application café.'
        },
        {
          image: 'coffee1.jpg',
          alt: 'Image de présentation de l’application café.'
        },
        {
          image: 'coffee2.jpg',
          alt: 'Image de présentation de l’application café.'
        }
      ]
    })
    return { ...toRefs(state) }
  }
}
</script>
