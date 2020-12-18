<template
  ><div>
    <CoffeeDetails id="coffee-details" :coffee="coffeeSelect" />
    <transition-group
      name="fade"
      uk-grid
      class="uk-child-width-1-3@l uk-child-width-1-2@m uk-grid-match uk-grid-large uk-text-center uk-flex-center"
    >
      <div v-for="coffee in coffees" :key="coffee.node.id">
        <CoffeeItem
          :coffee="coffee.node"
          @display-details="displayDetails"
        ></CoffeeItem>
      </div>
    </transition-group>
  </div>
</template>

<script>
import { reactive, toRefs } from '@vue/composition-api'

import useCoffee from '@/composition/coffee/useCoffee'

import CoffeeItem from '@/components/Coffee/Order/Section/Coffee/CoffeeItem'
import CoffeeDetails from '@/components/Coffee/Order/Section/Coffee/CoffeeDetails'

export default {
  name: 'CoffeeList',
  components: {
    CoffeeItem,
    CoffeeDetails
  },
  setup () {
    const { coffees } = useCoffee()
    const state = reactive({
      coffeeSelect: {}
    })

    const displayDetails = (coffee) => {
      state.coffeeSelect = coffee

      // eslint-disable-next-line no-undef
      UIkit.modal('#coffee-details').show()
    }

    return { coffees, displayDetails, ...toRefs(state) }
  }
}
</script>
