<template>
  <main v-if="!loading">
    <OrderHeader :application="result.applicationBySlug" />
  </main>
</template>

<script>
import { useQuery } from '@vue/apollo-composable'
import ApplicationBySlug from '@/graphql/Application/ApplicationBySlug.gql'
import OrderHeader from '@/components/Application/Order/OrderHeader'

export default {
  setup (props) {
    const { result, loading } = useQuery(ApplicationBySlug, () => ({
      slug: props.applicationSlug
    }))
    return {
      result,
      loading
    }
  },
  props: {
    applicationSlug: {
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
