<template>
  <div>
    <div class="uk-text-center uk-margin-large-bottom uk-text-bold">
      <p><span class="uk-label">Prix de votre commande</span> {{ price }}€</p>
    </div>
    <transition-group
      name="fade"
      uk-grid
      class="uk-flex uk-flex-center uk-grid-large"
      id="order-list"
    >
      <div v-for="coffeeOrder in coffeesOrder" :key="coffeeOrder.id">
        <CoffeeOrderedItem :coffee="coffeeOrder" />
      </div>
    </transition-group>
  </div>
</template>

<script>
import useCoffee from '@/composition/coffee/useCoffee'

import CoffeeOrderedItem from '@/components/Coffee/Order/Section/Order/CoffeeOrderedItem.vue'

export default {
  name: 'CoffeeOrderedList',
  components: { CoffeeOrderedItem },
  setup () {
    const { coffeesOrder, price } = useCoffee()

    return { coffeesOrder, price }
  }
}
</script>
