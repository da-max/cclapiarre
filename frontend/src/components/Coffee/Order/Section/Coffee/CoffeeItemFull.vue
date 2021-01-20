<template>
  <UtilsCard>
    <template #header>
      <div>
        <h2 class="uk-card-title">
          {{ coffee.farmCoop }}
        </h2>
      </div>
    </template>
    <template #body>
      <CoffeeDetailsContent :coffee="coffee" />
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

import CoffeeDetailsContent from '@/components/Coffee/Order/Section/Coffee/CoffeeDetailsContent'
import UtilsButton from '@/components/Utils/UtilsButton'
import UtilsCard from '@/components/Utils/UtilsCard'

export default {
    name: 'CoffeeItemFull',
    components: {
        CoffeeDetailsContent,
        UtilsCard,
        UtilsButton
    },
    props: {
        coffee: {
            type: Object,
            required: true
        }
    },
    setup () {
        const { addCoffeeOrder, valide } = useCoffee()

        return { addCoffeeOrder, valide }
    }
}
</script>
