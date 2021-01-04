<template>
  <UtilsModal
    :center="true"
    :container="true"
    :bg-close="true"
  >
    <template
      v-if="Object.keys(coffee).length !== 0"
      #header
    >
      <h3 class="uk-modal-title">
        {{ coffee.farmCoop }}
      </h3>
    </template>
    <template
      v-if="Object.keys(coffee).length !== 0"
      #body
    >
      <CoffeeDetailsContent :coffee="coffee" />
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          class="uk-modal-close"
          type="default"
        >
          Fermer
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import CoffeeDetailsContent from '@/components/Coffee/Order/Section/Coffee/CoffeeDetailsContent'

import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
  name: 'CoffeeDetails',
  components: {
    UtilsModal,
    UtilsButton,
    CoffeeDetailsContent
  },
  props: {
    coffee: {
      required: true,
      type: Object
    }
  }
}
</script>
