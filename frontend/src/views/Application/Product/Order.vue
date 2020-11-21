<template>
  <main v-if="!loading">
    <OrderHeader
      @update-description="updateDescription"
      :application="application"
    />
    <div
      class="uk-width-2-5@l uk-width4-5@s uk-margin-auto uk-margin-large-bottom"
    >
      <Alerts />
    </div>
    <div class="uk-text-center">
      <a
        class="uk-button uk-button-secondary"
        v-show="isAdmin($route.params.application)"
        type="secondary"
        :href="'/' + $route.params.application + '/recapitulatif'"
        >Générer le récapitulatif de la commande</a
      >
    </div>
    <OrderSection
      :applicationId="application.id"
      :products="application.products.edges"
      class="uk-margin-xlarge-top uk-width-4-5@m uk-margin-auto"
    />
  </main>
</template>

<script>
import store from '@/store/index'

import { useSetupTitle } from '@/composition/useUtils'

import Alerts from '@/components/Utils/Alert/Alerts'
import useApplication from '@/composition/useApplication'
import OrderHeader from '@/components/Application/Order/OrderHeader'
import OrderSection from '@/components/Application/Order/OrderSection'

export default {
  name: 'Order',
  setup (props) {
    const {
      application,
      loading,
      error,
      getApplication,
      updateApplication
    } = useApplication()

    useSetupTitle('Commander')
    getApplication(() => ({ slug: props.applicationSlug }))
    const updateDescription = function (newDescription) {
      updateApplication({
        id: application.value.id,
        name: application.value.name,
        description: newDescription
      })
    }

    const isAdmin = (application) => store.getters['application/isAdmin'](application)

    return {
      application,
      loading,
      error,
      updateDescription,
      isAdmin
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
}
</script>
