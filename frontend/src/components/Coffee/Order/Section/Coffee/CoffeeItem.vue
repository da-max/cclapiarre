<template>
  <UtilsCard mediaPos="bottom">
    <template #media>
      <div class="uk-transition-toggle uk-inline-clip" tabindex="0">
        <img
          v-if="coffee.image"
          :src="'/media/' + coffee.image"
          alt="Image de café"
        />
        <img
          v-else
          src="/static/Images/Coffee/coffee-global.jpg"
          alt="Image de café"
        />
        <div
          @click="$emit('display-details', coffee)"
          class="uk-flex uk-flex-middle uk-flex-center uk-transition-fade uk-position-cover uk-overlay uk-overlay-default uk-overflow-auto"
        >
          <p class="uk-text-large">En savoir plus ...</p>
        </div>
      </div>
    </template>
    <template #body>
      <h2 class="uk-card-title">{{ coffee.farmCoop }}</h2>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton>Ajouter ce produit à ma commande</UtilsButton>
      </div>
    </template>
  </UtilsCard>
</template>

<script>
import UtilsCard from '@/components/Utils/UtilsCard'
import UtilsButton from '@/components/Utils/UtilsButton.vue'

export default {
  name: 'CoffeeItem',
  props: {
    coffee: {
      required: true,
      type: Object
    }
  },
  components: {
    UtilsCard,
    UtilsButton
  },
  setup () {
    const log = () => console.log('hello world')

    return { log }
  }
}
</script>
