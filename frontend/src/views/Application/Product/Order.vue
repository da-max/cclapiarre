<template>
  <main v-if="!loading">
    <OrderHeader
      @update-description="updateDescription"
      :application="application"
    />
    <div class="uk-width-2-5@l uk-width4-5@s uk-margin-auto">
      <Alerts />
    </div>
    <OrderSection
      :products="application.products.edges"
      class="uk-margin-xlarge-top uk-width-4-5@m uk-margin-auto"
    />
  </main>
</template>

<script>
import Alerts from '@/components/Utils/Alert/Alerts'
import useApplication from '@/composition/useApplication'
import OrderHeader from '@/components/Application/Order/OrderHeader'
import OrderSection from '@/components/Application/Order/OrderSection'

export default {
  name: 'Order',
  setup (props) {
    const { application, loading, error, getApplication, updateApplication } = useApplication()
    getApplication(() => ({ slug: props.applicationSlug }))
    console.log(props)
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
    OrderSection,
    Alerts
  }
  // watch: {
  //   $route (to, from) {
  //     console.log(this.slug)
  //     this.slug = to.params.application
  //   }
  // }
}
</script>
