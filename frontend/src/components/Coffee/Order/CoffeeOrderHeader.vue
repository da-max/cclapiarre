<template>
  <header class="uk-margin-large-top">
    <h1 class="uk-text-center">
      Café
    </h1>
    <CoffeeOrderHeaderImage
      class="uk-margin-large-top uk-margin-auto uk-width-1-2@l uk-width-4-5@m"
    />
    <CoffeeOrderHeaderSection
      class="uk-margin-xlarge-top uk-width-3-5@m uk-margin-auto"
    />
  </header>
</template>

<script>
import CoffeeOrderHeaderImage from '@/components/Coffee/Order/Header/CoffeeOrderHeaderImage'
import CoffeeOrderHeaderSection from '@/components/Coffee/Order/Header/CoffeeOrderHeaderSection'

export default {
  components: { CoffeeOrderHeaderImage, CoffeeOrderHeaderSection }
}
</script>
