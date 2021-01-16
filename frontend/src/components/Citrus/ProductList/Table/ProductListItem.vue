<template>
  <tr>
    <td>
      <input
        v-model="checkProduct"
        type="checkbox"
        :title="`Sélectionner le produit ${product.node.name.toLowerCase()}`"
        class="uk-checkbox"
      >
    </td>
    <td>
      <UtilsButton
        type="default"
      >
        {{ product.node.name }}
      </UtilsButton>
      <CitrusDetails :product="product" />
    </td>
    <td>{{ product.node.weight !== 1 ? product.node.weight + 'kg' : 'Vendu à l’unité' }}</td>
    <td>{{ product.node.price }} €</td>
    <td><span :uk-icon="product.node.display ? 'check' : 'close'" /></td>
    <td><span :uk-icon="product.node.maybeNotAvailable ? 'check' : 'close'" /></td>
    <td>
      <button
        class="uk-icon-link"
        uk-icon="refresh"
        @click.prevent="showUpdateModal"
      /><button
        class="uk-icon-link"
        uk-icon="trash"
        @click.prevent="showDeleteModal"
      />
    </td>
  </tr>
</template>

<script>
import { computed } from '@vue/composition-api'

import useCitrus from '@/composition/citrus/useCitrus'
import { useShowModal } from '@/composition/useUtils'

import CitrusDetails from '@/components/Citrus/CitrusDetails'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
  name: 'ProductListItem',
  components: {
    CitrusDetails,
    UtilsButton
  },
  props: {
    productId: {
      required: true,
      type: String
    }
  },
  setup (props) {
    const { citrusById, setCheckCitrus, setCitrusSelect } = useCitrus()
    const product = computed(() => citrusById(props.productId))

    const checkProduct = computed({
      get: () => product.value.check,
      set: (value) => { setCheckCitrus(product.value, value) }
    })

    const showUpdateModal = () => {
      setCitrusSelect(product.value.node)
      useShowModal('#citrus-product-modal')
    }

    const showDeleteModal = () => {
      setCitrusSelect(product.value.node)
      useShowModal('#citrus-product-delete')
    }

    return {
      product,
      checkProduct,
      showUpdateModal,
      showDeleteModal
    }
  }
}
</script>
