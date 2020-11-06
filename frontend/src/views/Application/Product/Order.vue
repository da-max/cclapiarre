<template>
  <main v-if="!loading">
    <OrderHeader
      @update-description="updateDescription"
      :application="application"
    />
    <OrderSection
      :products="application.products.edges"
      class="uk-margin-large-top uk-width-4-5@m uk-margin-auto"
    />
  </main>
</template>

<script>
import useApplication from '@/composition/useApplication'
import OrderHeader from '@/components/Application/Order/OrderHeader'
import OrderSection from '@/components/Application/Order/OrderSection'
// import { useResult } from '@vue/apollo-composable'

export default {
  name: 'Order',
  setup (props) {
    const { application, loading, error, getApplication, updateApplication } = useApplication()
    getApplication({ slug: props.applicationSlug })
    console.log(application)
    const updateDescription = function (newDescription) {
      updateApplication({
        id: application.value.id,
        name: application.value.name,
        description: newDescription
      })
    }

    return {
      application,
      loading,
      error,
      updateDescription
    }
  },
  props: {
    applicationSlug: {
      required: true
    }
  },
  components: {
    OrderHeader,
    OrderSection
  }
}
</script>
