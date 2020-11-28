<template>
  <main>
    <OrderHeader />
    <div
      class="uk-width-2-5@l uk-width4-5@s uk-margin-auto uk-margin-large-bottom"
    >
      <Alerts />
    </div>
    <OrderSection
      class="uk-margin-xlarge-top uk-width-4-5@m uk-margin-auto"
    />
    <router-view name="modal"></router-view>
  </main>
</template>

<script>
import { useSetupTitle } from '@/composition/useUtils'
import useApplication from '@/composition/application/useApplication'

import Alerts from '@/components/Utils/Alert/Alerts'
import OrderHeader from '@/components/Application/Order/OrderHeader'
import OrderSection from '@/components/Application/Order/OrderSection'
import { computed } from '@vue/composition-api'

export default {
  name: 'Order',
  setup (props, { root }) {
    const application = computed(() => root.$route.params.application)
    const { getApplication } = useApplication(application)

    useSetupTitle('Commander')

    getApplication()

    return {
      getApplication
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
  },
  watch: {
    $route (to, from) {
      console.log('route')
      this.getApplication()
    }
  }
}
</script>
