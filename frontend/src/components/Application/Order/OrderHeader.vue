<template>
  <header class="uk-margin-large-top">
    <h1 class="uk-text-center">
      {{ application.name }}
    </h1>
    <OrderHeaderImage
      class="uk-margin-large-top uk-margin-auto uk-width-1-2@l uk-width-4-5@m"
    />
    <OrderHeaderSection
      class="uk-margin-xlarge-top uk-width-3-5@m uk-margin-auto"
    />
  </header>
</template>

<script>
import store from '@/store/index'

import OrderHeaderImage from '@/components/Application/Order/Header/OrderHeaderImage'
import OrderHeaderSection from '@/components/Application/Order/Header/OrderHeaderSection'
import { computed } from '@vue/composition-api'

export default {
  name: 'OrderHeader',
  setup () {
    const application = computed(() => store.state.application.currentApplication)

    return { application }
  },
  components: {
    OrderHeaderImage,
    OrderHeaderSection
  }
}
</script>
