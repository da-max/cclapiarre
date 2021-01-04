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
  components: {
    OrderHeader,
    OrderSection,
    Alerts
  },
  props: {
    applicationSlug: {
      required: true,
      type: String
    }
  },
  setup (props, { root }) {
    const application = computed(() => root.$route.params.application)
    const { getApplication } = useApplication(application)

    useSetupTitle('Commander')

    getApplication()

    return {
      getApplication
    }
  },
  watch: {
    $route (to, from) {
      this.getApplication()
    }
  }
}
</script>
