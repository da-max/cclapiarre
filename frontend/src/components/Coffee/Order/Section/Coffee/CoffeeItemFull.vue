<template>
  <UtilsCard>
    <template #header>
      <div>
        <h2 class="uk-card-title">{{ coffee.farmCoop }}</h2>
      </div>
    </template>
    <template #body>
      <CoffeeDetailsContent :coffee="coffee" />
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton @click="addCoffeeOrder(coffee)" id="add-coffee-button"
          >Commander ce café</UtilsButton
        >
      </div>
    </template>
  </UtilsCard>
</template>

<script>
import useCoffee from '@/composition/coffee/useCoffee'

import CoffeeDetailsContent from '@/components/Coffee/Order/Section/Coffee/CoffeeDetailsContent'
import UtilsButton from '@/components/Utils/UtilsButton'
import UtilsCard from '@/components/Utils/UtilsCard'

export default {
  name: 'CoffeeItemFull',
  props: {
    coffee: {
      type: Object,
      required: true
    }
  },
  components: {
    CoffeeDetailsContent,
    UtilsCard,
    UtilsButton
  },
  setup () {
    const { addCoffeeOrder } = useCoffee()

    return { addCoffeeOrder }
  }
}
</script>
