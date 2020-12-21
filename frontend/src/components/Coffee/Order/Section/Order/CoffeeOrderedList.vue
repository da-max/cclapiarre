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
    <div class="uk-text-center uk-margin-medium-top" v-show="coffeesOrder.length !== 0">
      <UtilsButton type="secondary" class="uk-margin-large-right" @click="showModal('#sommary-modal')"
        >Récapitulatif de la commande</UtilsButton
      >
      <UtilsButton @click="saveOrder">Commander</UtilsButton>
    </div>
  </div>
</template>

<script>
import useCoffee from '@/composition/coffee/useCoffee'
import { useShowModal } from '@/composition/useUtils'

import CoffeeOrderedItem from '@/components/Coffee/Order/Section/Order/CoffeeOrderedItem.vue'
import UtilsButton from '@/components/Utils/UtilsButton.vue'

export default {
  name: 'CoffeeOrderedList',
  components: { CoffeeOrderedItem, UtilsButton },
  setup () {
    const { coffeesOrder, price, saveOrder } = useCoffee()

    return { coffeesOrder, price, showModal: useShowModal, saveOrder }
  }
}
</script>
