<template>
  <UtilsCard
    :header="false"
    :footer="false"
    class="uk-margin-medium-bottom uk-padding"
  >
    <template #body>
      <form class="uk-form-horizontal">
        <div class="uk-margin-medium-bottom">
          <label
            for="farmCoop"
            class="uk-form-label"
          >Café</label>
          <div class="uk-form-controls">
            <select
              id="farmCoop"
              v-model="coffeeCoffee"
              name="farmCoop"
              class="uk-select"
            >
              <option
                v-for="c in coffees"
                :key="c.node.id"
                :value="c.node.id"
              >
                {{ c.node.farmCoop }}
              </option>
            </select>
          </div>
        </div>
        <div class="uk-margin-medium-bottom">
          <label
            for="weight"
            class="uk-form-label"
          >Poids du café</label>
          <div class="uk-form-controls">
            <select
              id="weight"
              v-model="coffeeWeight"
              name="weight"
              class="uk-select"
            >
              <option :value="null">
                Sélectionner le poids
              </option>
              <option value="200">
                200 grammes
              </option>
              <option value="1000">
                1 kilogramme
              </option>
            </select>
          </div>
        </div>
        <div
          v-show="coffee.weight !== null"
          class="uk-margin-medium-bottom"
        >
          <label
            for="type"
            class="uk-form-label"
          >Type de mouture</label>
          <div class="uk-form-controls">
            <select
              id="type"
              v-model="coffeeType"
              name="type"
              class="uk-select"
            >
              <option
                :value="null"
              >
                Sélectionner le type de mouture
              </option>
              <option
                v-for="type in coffee.coffee.availableType.edges"
                :key="type.node.id"
                :value="type.node"
              >
                {{ type.node.name }}
              </option>
            </select>
          </div>
        </div>
        <FormInputNumber
          v-show="coffee.weight !== null && coffee.type !== null"
          label="Quantité commandé"
          :value="coffee.amount"
          name="amount"
          @input="changeAmount"
        />
        <div class="uk-text-center">
          <UtilsButton
            type="danger"
            @click="removeCoffeeOrder(coffee.id)"
          >
            Supprimer de ma commande
          </UtilsButton>
        </div>
      </form>
    </template>
  </UtilsCard>
</template>

<script>
import useCoffee from '@/composition/coffee/useCoffee'

import UtilsCard from '@/components/Utils/UtilsCard.vue'
import UtilsButton from '@/components/Utils/UtilsButton.vue'
import FormInputNumber from '@/components/Utils/Form/FormInputNumber.vue'
import { computed } from '@vue/composition-api'

export default {
  name: 'CoffeeOrderedItem',
  components: {
    UtilsCard,
    UtilsButton,
    FormInputNumber
  },
  props: {
    coffee: {
      required: true,
      type: Object
    }
  },
  setup (props) {
    const { coffees, setAmount, removeCoffeeOrder, setCoffee, setType, setWeight } = useCoffee()

    const coffeeType = computed({
      get: () => props.coffee.type,
      set: (newType) => setType(props.coffee.id, newType)
    })

    const coffeeWeight = computed({
      get: () => props.coffee.weight,
      set: (newWeight) => setWeight(props.coffee.id, newWeight)
    })

    const coffeeCoffee = computed({
      get: () => props.coffee.coffee.id,
      set: (newCoffee) => setCoffee(props.coffee.id, newCoffee)
    })

    const changeAmount = (amount) => {
      setAmount(props.coffee.id, amount)
    }

    return { changeAmount, coffees, removeCoffeeOrder, coffeeType, coffeeWeight, coffeeCoffee }
  }
}
</script>
