import { onMounted } from '@vue/composition-api'

export function useSetupTitle (title = '') {
  onMounted(() => {
    document.title = `${title} | CC La Piarre`
  })
}
