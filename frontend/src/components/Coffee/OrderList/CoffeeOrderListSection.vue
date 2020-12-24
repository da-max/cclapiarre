<template>
  <section
    class="uk-margin-medium-top uk-width-1-2@m uk-margin-auto"
    v-if="!loading"
  >
    <UtilsCard v-for="order in orders.edges" :key="order.node.id">
      <template #header>
        <div class="uk-flex uk-flex-center uk-grid-large">
          <div>
            <span class="uk-label">Prénom</span>
            {{ order.node.user.firstName || 'Non défini' }}
          </div>
          <div>
            <span class="uk-label">Nom</span>
            {{ order.node.user.lastName || 'Non défini' }}
          </div>
          <div>
            <span class="uk-label">Email</span> {{ order.node.user.email }}
          </div>
          <div>
            <span class="uk-label">Prix total</span> {{ totalPrice(order.node.id) }}€
          </div>
        </div>
      </template>
      <template #body>
        <ul class="uk-list uk-list-striped">
          <li
            v-for="amount in order.node.amounts.edges"
            :key="amount.node.id"
            class="uk-flex uk-flex-between"
          >
            <div>
              <UtilsButton @click="displayDetails(amount.node.coffee)" type="text">{{ amount.node.coffee.farmCoop }}</UtilsButton> ({{ amount.node.sort.name }})
            </div>
            <div>
              {{
                amount.node.weight === 'A_200' ? '200 grammes' : '1 kilogramme'
              }}
              ×
              {{ amount.node.amount }} =
              {{
                amount.node.weight === 'A_200'
                  ? amount.node.amount * amount.node.coffee.twoHundredGramPrice
                  : amount.node.amount * amount.node.coffee.kilogramPrice
              }}€
            </div>
          </li>
        </ul>
      </template>
    </UtilsCard>
    <CoffeeDetails id="coffee-details" :coffee="coffeeSelect" />
  </section>
</template>

<script>
import { useResult } from '@vue/apollo-composable'
import { useUtilsQuery } from '@/composition/useUtils'
import useCoffee from '@/composition/coffee/useCoffee'

import UtilsCard from '@/components/Utils/UtilsCard.vue'
import UtilsButton from '@/components/Utils/UtilsButton.vue'
import CoffeeDetails from '@/components/Coffee/Order/Section/Coffee/CoffeeDetails'

import ORDER_ALL from '@/graphql/Coffee/Order/OrderAll.gql'

export default {
  name: 'CoffeeOrderListSection',
  components: { UtilsCard, UtilsButton, CoffeeDetails },
  setup () {
    const { coffeeSelect, displayDetails } = useCoffee()

    const { result, loading } = useUtilsQuery(ORDER_ALL)
    const orders = useResult(result)

    const totalPrice = (orderId) => {
      let price = 0
      const order = orders.value.edges.find((o) => o.node.id === orderId)
      order.node.amounts.edges.forEach(amount => {
        console.log(amount)
        if (amount.node.weight === 'A_200') {
          price += amount.node.amount * amount.node.coffee.twoHundredGramPrice
        } else {
          price += amount.node.amount * amount.node.coffee.kilogramPrice
        }
      })
      return price
    }

    return { orders, loading, totalPrice, coffeeSelect, displayDetails }
  }
}
</script>
