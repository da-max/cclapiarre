<template>
  <UtilsCard>
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
          <span class="uk-label">Prix total</span>
          {{ totalPrice }}€
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
            <UtilsButton
              type="text"
              @click="$emit('display-details', amount.node.coffee)"
            >
              {{ amount.node.coffee.farmCoop }}
            </UtilsButton>
            ({{ amount.node.sort.name }})
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
    <template #footer>
      <div class="uk-flex uk-flex-center">
        <UtilsButton
          type="danger"
          @click="useUtilsMutation(orderRemove, {orderId: order.node.id})"
        >
          Supprimer
        </UtilsButton>
      </div>
    </template>
  </UtilsCard>
</template>

<script>
import { computed } from '@vue/composition-api'
import { useUtilsMutation } from '@/composition/useUtils'
import useCoffee from '@/composition/coffee/useCoffee'
import store from '@/store/index'

import UtilsCard from '@/components/Utils/UtilsCard.vue'
import UtilsButton from '@/components/Utils/UtilsButton.vue'

export default {
  name: 'CoffeeOrderListItem',
  components: {
    UtilsCard,
    UtilsButton
  },
  props: {
    order: {
      required: true,
      type: Object
    }
  },
  setup (props, { emit }) {
    const { orderRemove: remove, onDoneRemoveOrder } = useCoffee()

    const totalPrice = computed(() => {
      let price = 0
      props.order.node.amounts.edges.forEach(amount => {
        if (amount.node.weight === 'A_200') {
          price += amount.node.amount * amount.node.coffee.twoHundredGramPrice
        } else {
          price += amount.node.amount * amount.node.coffee.kilogramPrice
        }
      })
      return price
    })

    const orderRemove = () => {
      remove({ orderId: props.order.node.id })
    }

    onDoneRemoveOrder((result) => {
      if (result.data.removeCoffeeOrder.found) {
        emit('order-delete')
        store.commit('alert/ADD_ALERT', {
          header: true,
          headerContent: 'Commande supprimée',
          body: 'La commande séléctionnée a bien été supprimé.',
          status: 'success',
          close: true
        })
      } else {
        store.commit('alert/ADD_ALERT', {
          header: true,
          headerContent: 'Commande non trouvé',
          body: 'La commande séléctionnée n’a pas pu être supprimé, car elle n’a pas été trouvé. Merci de réessayer.',
          status: 'warning',
          close: true
        })
      }
    })

    return {
      totalPrice,
      useUtilsMutation,
      orderRemove
    }
  }
}
</script>
