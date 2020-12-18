<template>
    <main>
      <CoffeeOrderHeader />
      <CoffeeOrderSection />
    </main>
</template>

<script>
import CoffeeOrderHeader from '@/components/Coffee/Order/CoffeeOrderHeader.vue'
import CoffeeOrderSection from '@/components/Coffee/Order/CoffeeOrderSection'

export default {
  name: 'CoffeeOrder',
  components: {
    CoffeeOrderHeader,
    CoffeeOrderSection
  }
}
</script>
