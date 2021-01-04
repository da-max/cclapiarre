<template>
  <div>
    <div class="uk-text-center uk-margin-large-bottom uk-text-bold">
      <p><span class="uk-label">Prix de votre commande</span> {{ price }}€</p>
    </div>
    <transition-group
      id="order-list"
      name="fade"
      uk-grid
      class="uk-flex uk-flex-center uk-grid-large"
    >
      <div
        v-for="coffeeOrder in coffeesOrder"
        :key="coffeeOrder.id"
      >
        <CoffeeOrderedItem :coffee="coffeeOrder" />
      </div>
    </transition-group>
    <div
      v-show="coffeesOrder.length !== 0"
      class="uk-text-center uk-margin-medium-top"
    >
      <UtilsButton
        type="secondary"
        class="uk-margin-large-right"
        :disabled="!valide"
        @click="showModal('#sommary-modal')"
      >
        Récapitulatif de la commande
      </UtilsButton>
      <UtilsButton
        :disabled="!valide"
        @click="saveOrder"
      >
        Commander
      </UtilsButton>
    </div>
    <CoffeeOrderedSommary id="sommary-modal" />
  </div>
</template>

<script>
import useCoffee from '@/composition/coffee/useCoffee'
import { useShowModal } from '@/composition/useUtils'

import CoffeeOrderedItem from '@/components/Coffee/Order/Section/Order/CoffeeOrderedItem.vue'
import UtilsButton from '@/components/Utils/UtilsButton.vue'
import CoffeeOrderedSommary from './CoffeeOrderedSommary.vue'

export default {
  name: 'CoffeeOrderedList',
  components: { CoffeeOrderedItem, UtilsButton, CoffeeOrderedSommary },
  setup () {
    const { coffeesOrder, price, saveOrder, valide } = useCoffee()

    return { coffeesOrder, price, showModal: useShowModal, saveOrder, valide }
  }
}
</script>
