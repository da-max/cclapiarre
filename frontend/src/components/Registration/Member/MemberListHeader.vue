<template>
  <header>
    <h1 class="uk-text-center">
      Liste des adhérents
    </h1>
    <div class="uk-text-center uk-margin-large">
      <UtilsButton @click="showMemberModal">
        Ajouter un adhérent
      </UtilsButton>
    </div>
  </header>
</template>

<script>
import useMember from '@/composition/registration/useMember'

import UtilsButton from '@/components/Utils/UtilsButton'

export default {
    name: 'MemberListHeader',
    components: {
        UtilsButton
    },
    setup () {
        const { showMemberModal } = useMember()

        return { showMemberModal }
    }
}
</script>
