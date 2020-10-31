<template>
  <main v-if="response.loading === false">
    <OrderHeader :application="response.data.applicationBySlug" />
  </main>
</template>

<script>
import { useDataFetcher } from '@/composition/useDataFetcher'
import ApplicationBySlug from '@/graphql/Application/ApplicationBySlug.gql'

import OrderHeader from '@/components/Application/Order/OrderHeader'

export default {
  setup (props) {
    console.log(props)
    const { error, response } = useDataFetcher({
      query: ApplicationBySlug,
      variables: { slug: props.application }
    })
    return {
      error,
      response
    }
  },
  props: {
    application: {
      required: true
    }
  },
  data () {
    return {
      query: ApplicationBySlug
    }
  },
  components: {
    OrderHeader
  }
}
</script>
