<template>
  <UtilsModal
    v-if="canAddMember || canChangeMember"
    id="member-modal"
    :center="true"
    :container="true"
    :esc-close="false"
  >
    <template #header>
      <h2 class="uk-modal-title">
        {{ member.id ? 'Modifier' : 'Ajouter' }} un membre
      </h2>
    </template>
    <template #body>
      <MemberForm />
    </template>
    <template #footer>
      <div class="uk-text-center">
        <UtilsButton
          type="secondary"
          class="uk-modal-close"
        >
          Annuler
        </UtilsButton>
        <UtilsButton
          type="primary"
          class="uk-margin-medium-left"
          :disabled="!memberValide"
          @click="saveMember"
        >
          {{ member.id ? 'Modifier': 'Ajouter' }}
        </UtilsButton>
      </div>
    </template>
  </UtilsModal>
</template>

<script>
import useMember from '@/composition/registration/useMember'

import MemberForm from '@/components/Registration/Member/MemberForm'
import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsButton from '@/components/Utils/UtilsButton.vue'

export default {
    name: 'MemberModal',
    components: {
        MemberForm,
        UtilsButton,
        UtilsModal
    },
    setup () {
        const {
            canAddMember,
            canChangeMember,
            member,
            memberValide,
            saveMember
        } = useMember()

        return {
            canAddMember,
            canChangeMember,
            member,
            memberValide,
            saveMember
        }
    }
}
</script>
