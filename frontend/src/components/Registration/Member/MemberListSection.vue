<template>
  <div class="uk-card uk-card-default">
    <div class="uk-card-body">
      <MemberDeleteModal />
      <MemberModal />
      <MemberTable />
    </div>
    <div class="uk-card-footer">
      <p class="uk-text-bold">
        Si vous voyez une erreur, merci de me la signaler en envoyant un mail à
        maxime.benhassen@tutamail.com
      </p>
    </div>
  </div>
</template>

<script>
import MemberTable from '@/components/Registration/Member/MemberTable'
import MemberModal from '@/components/Registration/Member/MemberModal'
import MemberDeleteModal from '@/components/Registration/Member/MemberDeleteModal'

export default {
    name: 'MemberListSection',
    components: {
        MemberModal,
        MemberTable,
        MemberDeleteModal
    }
}
</script>
