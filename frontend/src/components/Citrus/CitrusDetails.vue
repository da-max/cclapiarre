<template>
  <UtilsDrop :mode="mode">
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
</template>

<script>
import UtilsDrop from '@/components/Utils/UtilsDrop'

export default {
    name: 'CitrusDetails',
    components: {
        UtilsDrop
    },
    props: {
        product: {
            required: true,
            type: Object
        },
        mode: {
            required: false,
            type: String,
            default: 'click'
        }
    }
}
</script>
