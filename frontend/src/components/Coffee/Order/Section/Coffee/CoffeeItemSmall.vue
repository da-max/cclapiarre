<template>
  <UtilsCard media-pos="bottom">
    <template #media>
      <div
        class="uk-transition-toggle uk-inline-clip"
        tabindex="0"
      >
        <img
          v-if="coffee.image"
          :src="'/media/' + coffee.image"
          alt="Image de café"
        >
        <img
          v-else
          src="/static/Images/Coffee/coffee-global.jpg"
          alt="Image de café"
        >
        <div
          class="uk-flex uk-flex-middle uk-flex-center uk-transition-fade uk-position-cover uk-overlay uk-overlay-default uk-overflow-auto"
          @click="$emit('display-details', coffee)"
        >
          <p class="uk-text-large">
            En savoir plus ...
          </p>
        </div>
      </div>
    </template>
    <template #body>
      <h2 class="uk-card-title">
        {{ coffee.farmCoop }}
      </h2>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          id="add-coffee-button"
          :disabled="!valide"
          @click="addCoffeeOrder(coffee)"
        >
          Commander ce café
        </UtilsButton>
      </div>
    </template>
  </UtilsCard>
</template>

<script>
import useCoffee from '@/composition/coffee/useCoffee'

import UtilsCard from '@/components/Utils/UtilsCard'
import UtilsButton from '@/components/Utils/UtilsButton.vue'

export default {
  name: 'CoffeeItemSmall',
  components: {
    UtilsCard,
    UtilsButton
  },
  props: {
    coffee: {
      required: true,
      type: Object
    }
  },
  setup () {
    const { addCoffeeOrder, valide } = useCoffee()

    return { addCoffeeOrder, valide }
  }
}
</script>
