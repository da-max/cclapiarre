<template>
  <UtilsTable>
    <template #head>
      <th>
        <input
          v-model="checkAll"
          type="checkbox"
          title="Sélectionner tous les produits"
          class="uk-checkbox"
        >
      </th>
      <th>Nom du produit</th>
      <th>
        <span :uk-tooltip="`title: ${tooltip.weight}`">
          Poids du produit
        </span>
      </th>
      <th>Prix du produit</th>
      <th>
        <span :uk-tooltip="`title: ${tooltip.display}`">
          Produit affiché
        </span>
      </th>
      <th>
        <span :uk-tooltip="`title: ${tooltip.maybeNotAvailable}`">
          Produit peut être indisponible
        </span>
      </th>
      <th>Actions</th>
    </template>
    <template #body>
      <ProductListItem
        v-for="product in citrus"
        :key="product.node.id"
        :product-id="product.node.id"
      />
    </template>
  </UtilsTable>
</template>

<script>
import { reactive, toRefs } from '@vue/composition-api'
import useCitrus from '@/composition/citrus/useCitrus'

import ProductListItem from '@/components/Citrus/ProductList/Table/ProductListItem'
import UtilsTable from '@/components/Utils/UtilsTable'

export default {
    name: 'ProductListTable',
    components: {
        ProductListItem,
        UtilsTable
    },
    setup () {
        const state = reactive({
            tooltip: {
                weight: 'Si le poids du produit est de 1, cela veut dire que le produit ne se vend pas au poids, mais à l’unité.',
                display: 'Défini si ce produit est affiché, ou pas, sur le tableau des commandes.',
                maybeNotAvailable: 'Permet d’afficher un message d’alerte sur le tableau de commande, afin de prévenir les adhérents que le produit ne sera, peut-être, pas disponible.'
            }
        })
        const { checkAll, searchCitrus } = useCitrus()

        return { ...toRefs(state), checkAll, citrus: searchCitrus }
    }
}
</script>
