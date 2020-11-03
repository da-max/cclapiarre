<template>
  <main v-if="!loading">
    <OrderHeader :application="result.applicationBySlug" />
    <OrderSection
      :products="result.applicationBySlug.products.edges"
      class="uk-margin-large-top uk-width-4-5@m uk-margin-auto"
    />
  </main>
</template>

<script>
import { useQuery } from '@vue/apollo-composable'
import ApplicationBySlug from '@/graphql/Application/ApplicationBySlug.gql'
import OrderHeader from '@/components/Application/Order/OrderHeader'
import OrderSection from '@/components/Application/Order/OrderSection'

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
    OrderHeader,
    OrderSection
  }
}
</script>
