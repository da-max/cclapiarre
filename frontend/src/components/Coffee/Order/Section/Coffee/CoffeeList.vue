<template
  ><div>
    <CoffeeDetails id="coffee-details" :coffee="coffeeSelect" />
    <form
      action="#"
      class="uk-form-horizontal uk-margin-large-bottom uk-width-1-3@m"
    >
      <label for="displaying" class="uk-form-label">Mode d’affichage</label>
      <div class="uk-form-controls">
        <select
          name="displaying"
          id="displaying"
          class="uk-select"
          v-model="displaying"
        >
          <option
            v-for="(val, text) in DISPLAYING_MODE"
            :value="val"
            :key="val"
            >{{ text }}</option
          >
        </select>
      </div>
    </form>
    <div
      v-if="displaying === 'small'"
      uk-grid
      class="uk-child-width-1-3@l uk-child-width-1-2@m uk-grid-match uk-grid-large uk-text-center uk-flex-center"
    >
      <div v-for="coffee in coffees" :key="coffee.node.id">
        <CoffeeItemSmall
          :coffee="coffee.node"
          @display-details="displayDetails"
        ></CoffeeItemSmall>
      </div>
    </div>
    <div v-else>
      <div
        v-for="coffee in coffees"
        :key="coffee.node.id"
        class="uk-margin-xlarge-bottom uk-width-5-6@m uk-margin-auto"
      >
        <CoffeeItemFull
          :coffee="coffee.node"
          @display-details="displayDetails"
        ></CoffeeItemFull>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, toRefs, onBeforeMount } from '@vue/composition-api'

import useCoffee from '@/composition/coffee/useCoffee'

import CoffeeItemSmall from '@/components/Coffee/Order/Section/Coffee/CoffeeItemSmall'
import CoffeeItemFull from '@/components/Coffee/Order/Section/Coffee/CoffeeItemFull'
import CoffeeDetails from '@/components/Coffee/Order/Section/Coffee/CoffeeDetails'

export default {
  name: 'CoffeeList',
  components: {
    CoffeeItemSmall,
    CoffeeItemFull,
    CoffeeDetails
  },
  setup () {
    const { coffees, getCoffees } = useCoffee()
    const state = reactive({
      coffeeSelect: {},
      displaying: 'small',
      DISPLAYING_MODE: {
        'Affichage réduit': 'small',
        'Afficher toutes les informations': 'full'
      }
    })

    const displayDetails = (coffee) => {
      state.coffeeSelect = coffee

      // eslint-disable-next-line no-undef
      UIkit.modal('#coffee-details').show()
    }

    onBeforeMount(() => getCoffees())

    return { coffees, displayDetails, ...toRefs(state) }
  }
}
</script>
