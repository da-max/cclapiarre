<template>
  <UtilsModal :container="true" :center="true">
    <template #header>
      <h2 class="uk-modal-title">Récapitulatif de la commande</h2>
    </template>
    <template #body>
      <UtilsTable>
        <template #head>
          <th>Produit</th>
          <th>Poids</th>
          <th>Option</th>
          <th>Quantité</th>
          <th>Prix</th>
          <th>Supprimer</th>
        </template>
        <template #body>
          <tr
            v-for="productOrdered in productsOrdered"
            :key="productOrdered.id"
          >
            <td>{{ productOrdered.product.name }}</td>
            <td>
              {{ productOrdered.weight.node.weight }}
              {{ productOrdered.weight.node.unit }}
            </td>
            <td v-if="productOrdered.option">
              {{ productOrdered.option.node.name }}
            </td>
            <td v-else>Non disponible</td>
            <td>
              <input
                type="number"
                name="amount"
                class="uk-input uk-form-width-small"
                v-model="productOrdered.amount"
              />
            </td>
            <td>{{ total(productOrdered.id) }} €</td>
            <td>
              <UtilsButton
                type="danger"
                width="small"
                @click="removeProduct(productOrdered.id)"
                >Supprimer</UtilsButton
              >
            </td>
          </tr>
        </template>
      </UtilsTable>
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton type="default" class="uk-modal-close">Annuler</UtilsButton>
        <UtilsButton type="primary" class="uk-margin-left" @click="addOrder" :disabled="!valide">Commander</UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsTable from '@/components/Utils/UtilsTable'
import UtilsButton from '@/components/Utils/UtilsButton'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
export default {
  name: 'ProductOrderedSommaryModal',
  components: {
    UtilsModal,
    UtilsTable,
    UtilsButton
  },
  computed: {
    ...mapState({ productsOrdered: (state) => state.order.order }),
    ...mapGetters({ total: 'order/uniqPrice', idApplicationBySlug: 'application/idApplicationBySlug', valide: 'order/valide' }),
    applicationId () {
      return this.idApplicationBySlug(this.$route.params.application)
    }
  },
  methods: {
    ...mapMutations({ removeProduct: 'order/REMOVE_PRODUCT_ORDER', setAmount: 'order/SET_AMOUNT' }),
    ...mapActions({ saveOrder: 'order/saveOrder' }),
    async addOrder () {
      // eslint-disable-next-line no-undef
      UIkit.modal('#sommaryModal').hide()
      await this.saveOrder(this.applicationId)
    }
  }
}
</script>

<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
