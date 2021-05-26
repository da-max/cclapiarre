import apolloClient from '@/vue-apollo'
import Vue from 'vue'

import MEMBER_ADD from '@/graphql/Member/MemberAdd.gql'
import MEMBER_ALL from '@/graphql/Member/MemberAll.gql'
import MEMBER_DELETE from '@/graphql/Member/MemberDelete.gql'
import MEMBER_UPDATE from '@/graphql/Member/MemberUpdate.gql'

export default {
    namespaced: true,

    state: () => ({
        memberSelect: {
            username: '',
            lastName: '',
            firstName: '',
            email: '',
            phoneNumber: '',
            password: '',
            passwordConfirm: '',
            userPermissions: [],
            groups: []
        },
        members: []
    }),

    mutations: {
        ADD_MEMBER (state, member) {
            state.members = [...state.members, member]
        },

        DELETE_MEMBER (state, memberId) {
            state.members = state.members.filter(m => m.id !== memberId)
        },

        SET_MEMBERS (state, members) {
            state.members = members
        },

        SET_MEMBER_SELECT (state, member) {
            if (member.information && member.information.phoneNumber) {
                state.memberSelect = {
                    ...member,
                    phoneNumber: member.information.phoneNumber,
                    information: null
                }
            } else if (!member.phoneNumber) {
                state.memberSelect = {
                    ...member,
                    phoneNumber: ''
                }
            } else {
                state.memberSelect = member
            }
        },

        SET_MEMBER_DEFAULT (state) {
            Vue.set(state, 'memberSelect', {
                username: '',
                lastName: '',
                firstName: '',
                password: '',
                passwordConfirm: '',
                email: '',
                phoneNumber: '',
                userPermissions: [],
                groups: []
            })
            Vue.set(state.memberSelect, 'userPermissions', [])
            Vue.set(state.memberSelect, 'groups', [])
        },

        UPDATE_MEMBER (state, member) {
            state.members = [
                member,
                ...state.members.filter((m) => m.id !== member.id)
            ]
        }
    },

    actions: {
        async getMembers ({ commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.query({
                    query: MEMBER_ALL
                })
                commit('SET_MEMBERS', response.data.users)
            } catch (e) {
                commit('alert/ADD_ERROR', e, { root: true })
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        },

        async saveMember ({ state, commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const member = {
                    username: state.memberSelect.username,
                    email: state.memberSelect.email,
                    firstName: state.memberSelect.firstName,
                    lastName: state.memberSelect.lastName,
                    password: state.memberSelect.password,
                    information: {
                        phoneNumber: state.memberSelect.phoneNumber
                    },
                    groups: state.memberSelect.groups,
                    userPermissions: state.memberSelect.userPermissions
                }

                const response = await apolloClient.mutate({
                    mutation: MEMBER_ADD,
                    variables: { input: member }
                })
                console.log(response.data)
                commit('ADD_MEMBER', response.data.addUser.user)
                commit(
                    'alert/ADD_ALERT',
                    {
                        header: false,
                        body: 'Le membre a bien été ajouté !',
                        status: 'success',
                        close: true
                    },
                    { root: true }
                )
            } catch (e) {
                commit('alert/ADD_ERROR', e, { root: true })
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        },

        async removeMember ({ state, commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.mutate({
                    mutation: MEMBER_DELETE,
                    variables: { id: state.memberSelect.id }
                })
                if (response.data.deleteUser.found) {
                    commit('DELETE_MEMBER', state.memberSelect.id)
                    commit('alert/ADD_ALERT', {
                        header: false,
                        body: 'L’adhérent a bien été supprimé.',
                        status: 'success',
                        close: true
                    }, { root: true })
                } else {
                    throw new Error('L’adhérent n’a pas été trouvé.')
                }
            } catch (e) {
                commit('alert/ADD_ERROR', e, { root: true })
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        },

        async updateMember ({ state, commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const groups = state.memberSelect.groups.map(g => {
                    if (Number.isInteger(g)) {
                        return g
                    } else {
                        return Number(g.id)
                    }
                })
                const permissions = state.memberSelect.userPermissions.map(p => {
                    if (Number.isInteger(p)) {
                        return p
                    } else {
                        return Number(p.id)
                    }
                })
                const member = {
                    username: state.memberSelect.username,
                    email: state.memberSelect.email,
                    firstName: state.memberSelect.firstName,
                    lastName: state.memberSelect.lastName,
                    information: {
                        phoneNumber: state.memberSelect.phoneNumber
                    },
                    groups: groups,
                    userPermissions: permissions
                }
                const response = await apolloClient.mutate({
                    mutation: MEMBER_UPDATE,
                    variables: {
                        id: state.memberSelect.id,
                        input: member
                    }
                })
                commit(
                    'alert/ADD_ALERT',
                    {
                        header: false,
                        body: 'Le membre a bien été modifié.',
                        status: 'success',
                        close: true
                    },
                    { root: true }
                )
                commit('SET_MEMBER_DEFAULT')
                commit('UPDATE_MEMBER', response.data.updateUser.user)
            } catch (e) {
                commit('alert/ADD_ERROR', e, { root: true })
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        }
    },
    getters: {
        memberValide: (state) => {
            return (
                state.memberSelect.username &&
                state.memberSelect.email &&
                (state.memberSelect.id ||
                    (state.memberSelect.password && state.memberSelect.password ===
                    state.memberSelect.passwordConfirm))
            )
        }
    }
}
