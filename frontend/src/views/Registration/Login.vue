<template>
  <div>
    <h1 class="uk-text-center uk-margin-large-top uk-margin-large-bottom">
      {{ title }}
    </h1>
    <LoginSection />
  </div>
</template>

<script>
import LoginSection from '@/components/Registration/Login/LoginSection'
import { useSetupTitle } from '@/composition/utils'

export default {
  setup (props) {
    const title = 'Se connecter'
    useSetupTitle(title)
    return {
      title
    }
  },
  components: {
    LoginSection
  }
}
</script>
