import { computed, ref } from '@vue/composition-api'
import store from '@/store/index'

export default function (applicationSlug) {
  const slug = ref(applicationSlug)

  const application = computed(() => store.state.application.currentApplication)

  const isAdmin = computed(() =>
    store.getters['application/isAdmin'](slug.value)
  )
  const products = computed(() => store.getters['application/products'])

  const updateApplication = () => {
    store.dispatch('application/saveApplication')
  }

  const getApplication = () => {
    store.dispatch('application/getCurrentApplication', slug.value)
  }

  return {
    updateApplication,
    getApplication,
    isAdmin,
    products,
    application
  }
}
