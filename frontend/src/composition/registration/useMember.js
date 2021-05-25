import { computed, reactive, toRefs } from '@vue/composition-api'

import { useHideModal, useShowModal, useUtilsQuery } from '@/composition/useUtils'
import store from '@/store/index'

import PERMISSION_ALL from '@/graphql/User/PermissionAll.gql'
import GROUP_ALL from '@/graphql/User/GroupAll.gql'
import { useResult } from '@vue/apollo-composable'

export default function () {
    // Store
    const state = reactive({
        permissions: [],
        groups: []
    })

    // State
    const member = computed(() => store.state.member.memberSelect)
    const members = computed(() => store.state.member.members)

    // Getters
    const memberValide = computed(() => store.getters['member/memberValide'])

    // Mutations
    const setMemberSelect = (member) => { store.commit('member/SET_MEMBER_SELECT', member) }
    const setMemberDefault = () => { store.commit('member/SET_MEMBER_DEFAULT') }

    // Actions
    const getMembers = () => { store.dispatch('member/getMembers') }
    const removeMember = () => { store.dispatch('member/removeMember') }

    // State

    // Permissions
    const canAddMember = computed(() => store.getters['auth/findPermission']('registration.add_information'))
    const canChangeMember = computed(() => store.getters['auth/findPermission']('registration.change_information'))
    const canDeleteMember = computed(() => store.getters['auth/findPermission']('registration.delete_information'))

    // Methods

    const getGroups = () => {
        const { result, loading } = useUtilsQuery(GROUP_ALL)
        state.groups = useResult(result)
        return { loading }
    }

    const getPermissions = () => {
        const { result, loading } = useUtilsQuery(PERMISSION_ALL)
        state.permissions = useResult(result)
        return { loading }
    }

    const saveMember = () => {
        useHideModal('#member-modal')
        if (member.value.id) {
            store.dispatch('member/updateMember')
        } else {
            store.dispatch('member/saveMember')
        }
    }

    const showDeleteMemberModal = (member) => {
        setMemberSelect(member)
        useShowModal('#member-delete-modal')
    }

    const showMemberModal = (member = undefined) => {
        if (member) {
            setMemberSelect(member)
        } else {
            setMemberDefault()
        }
        useShowModal('#member-modal')
    }

    const updateEmail = (e) => {
        setMemberSelect({ ...member.value, email: e })
    }
    const updateFirstName = (e) => {
        setMemberSelect({ ...member.value, firstName: e })
    }
    const updateGroup = (e) => {
        if (e.target.checked) {
            setMemberSelect({ ...member.value, groups: [...member.value.groups, Number(e.target.value)] })
        } else {
            const groups = member.value.groups.filter(up => up !== Number(e.target.value))
            setMemberSelect({ ...member.value, groups })
        }
    }
    const updateLastName = (e) => {
        setMemberSelect({ ...member.value, lastName: e })
    }
    const updatePassword = (e) => {
        setMemberSelect({ ...member.value, password: e })
    }
    const updatePasswordConfirm = (e) => {
        setMemberSelect({ ...member.value, passwordConfirm: e })
    }
    const updatePermission = (e) => {
        if (e.target.checked) {
            setMemberSelect({ ...member.value, userPermissions: [...member.value.userPermissions, Number(e.target.value)] })
        } else {
            const userPermissions = member.value.userPermissions.filter(up => up !== Number(e.target.value))
            setMemberSelect({ ...member.value, userPermissions })
        }
    }
    const updatePhoneNumber = (e) => {
        setMemberSelect({ ...member.value, phoneNumber: e })
    }
    const updateUsername = (e) => {
        setMemberSelect({ ...member.value, username: e })
    }

    return {
        member,
        members,

        memberValide,

        getMembers,
        removeMember,
        setMemberSelect,

        canAddMember,
        canChangeMember,
        canDeleteMember,

        ...toRefs(state),

        getGroups,
        getPermissions,

        showDeleteMemberModal,
        saveMember,
        showMemberModal,

        updateEmail,
        updateFirstName,
        updateGroup,
        updateLastName,
        updatePassword,
        updatePasswordConfirm,
        updatePermission,
        updatePhoneNumber,
        updateUsername
    }
}
