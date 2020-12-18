<template>
  <section class="uk-margin-medium-top">
    <OrderInformation class="uk-width-1-2@l uk-margin-auto" />
    <CoffeeList></CoffeeList>
  </section>
</template>

<script>
import OrderInformation from '@/components/Application/Order/Section/OrderInformation'
import CoffeeList from '@/components/Coffee/Order/Section/Coffee/CoffeeList'

export default {
  name: 'CoffeeOrderSection',
  components: {
    OrderInformation,
    CoffeeList
  }
}
</script>
