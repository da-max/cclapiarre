<template>
  <div class="uk-margin-large-top">
    <h1 class="uk-text-center">{{ title }}</h1>

    <MemberSection class="uk-width-3-5@l uk-width-4-5@s uk-margin-auto" />

  </div>
</template>

<script>
import MemberSection from '@/components/Registration/Member/MemberSection'
import { useSetupTitle } from '@/composition/useUtils'

export default {
  setup () {
    const title = 'Liste des adhérents'
    useSetupTitle(title)
    return { title }
  },
  components: {
    MemberSection
  }
}
</script>
