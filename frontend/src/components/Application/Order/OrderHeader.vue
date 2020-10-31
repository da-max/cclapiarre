<template>
  <header class="uk-margin-large-top">
    <h1 class="uk-text-center">
      {{ application.name }}
    </h1>
    <OrderHeaderImage
      class="uk-margin-large-top uk-margin-auto uk-width-1-2@l uk-width-4-5@m"
      :images="application.images"
    />
    <OrderHeaderSection
      class="uk-margin-xlarge-top uk-width-3-5@m uk-margin-auto"
      :description="application.description"
    />
  </header>
</template>

<script>
import OrderHeaderImage from '@/components/Application/Order/Header/OrderHeaderImage'
import OrderHeaderSection from '@/components/Application/Order/Header/OrderHeaderSection'

export default {
  name: 'OrderHeader',
  props: {
    application: {
      required: true,
      type: Object
    }
  },
  components: {
    OrderHeaderImage,
    OrderHeaderSection
  }
}
</script>
