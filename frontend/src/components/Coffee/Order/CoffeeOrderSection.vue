<template>
  <section class="uk-margin-medium-top uk-width-4-5@m uk-margin-auto">
    <OrderInformation class="uk-width-1-2@l uk-margin-auto" />
    <CoffeeOrderedList class="uk-margin-large-top" />
    <CoffeeList class="uk-margin-xlarge-top" />
  </section>
</template>

<script>
import OrderInformation from '@/components/Application/Order/Section/OrderInformation'
import CoffeeList from '@/components/Coffee/Order/Section/Coffee/CoffeeList'
import CoffeeOrderedList from '@/components/Coffee/Order/Section/Order/CoffeeOrderedList'

export default {
    name: 'CoffeeOrderSection',
    components: {
        OrderInformation,
        CoffeeList,
        CoffeeOrderedList
    }
}
</script>
