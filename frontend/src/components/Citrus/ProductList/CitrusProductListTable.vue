<template>
  <UtilsTable>
    <template #head>
      <th>
        <input
          v-model="checkAll"
          type="checkbox"
          class="uk-checkbox"
        >
      </th>
      <th>Nom du produit</th>
      <th>Poids du produit</th>
      <th>Prix du produit</th>
      <th>Produit affiché</th>
      <th>Produit peut être indisponible</th>
      <th>Actions</th>
    </template>
    <template #body>
      <tr
        v-for="product in citrus"
        :key="product.node.id"
      >
        <td>
          <input
            v-model="product.check"
            type="checkbox"
            class="uk-checkbox"
          >
        </td>
        <td>
          <UtilsButton
            type="default"
          >
            {{ product.node.name }}
          </UtilsButton>
          <UtilsDrop mode="click">
            <template #default>
              <div class="uk-card-header">
                <h5 class="uk-card-title">
                  {{ product.node.name.toLowerCase() }}
                </h5>
              </div>
              <div class="uk-card-body">
                Prix : {{ product.node.price }} €<br>
                Poids : {{ product.node.weight !== 1 ? product.node.weight + 'kg' : 'Vendu à l’unité' }}<br>
                <div
                  v-html="product.node.description"
                />
              </div>
            </template>
          </UtilsDrop>
        </td>
        <td>{{ product.node.weight !== 1 ? product.node.weight + 'kg' : 'Vendu à l’unité' }}</td>
        <td>{{ product.node.price }} €</td>
        <td><span :uk-icon="product.node.display ? 'check' : 'close'" /></td>
        <td><span :uk-icon="product.node.maybeNotAvailable ? 'check' : 'close'" /></td>
        <td>
          <a
            class="uk-icon-link"
            uk-icon="refresh"
          /><a
            class="uk-icon-link"
            uk-icon="trash"
          />
        </td>
      </tr>
    </template>
  </UtilsTable>
</template>

<script>
import useCitrus from '@/composition/citrus/useCitrus'

import UtilsButton from '@/components/Utils/UtilsButton'
import UtilsDrop from '@/components/Utils/UtilsDrop'
import UtilsTable from '@/components/Utils/UtilsTable'

export default {
  name: 'CitrusProductListTable',
  components: {
    UtilsButton,
    UtilsDrop,
    UtilsTable
  },
  setup () {
    const { checkAll, searchCitrus } = useCitrus()

    return { checkAll, citrus: searchCitrus }
  }
}
</script>
