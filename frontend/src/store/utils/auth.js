import apolloClient from '@/vue-apollo'

import USER_LOGIN from '@/graphql/User/UserLogin.gql'
import USER_LOGOUT from '@/graphql/User/UserLogout.gql'
import USER_CURRENT from '@/graphql/User/UserCurrent.gql'

export default {
    namespaced: true,
    state: () => {
        return { currentUser: null }
    },

    mutations: {
        LOGOUT_USER (state) {
            state.currentUser = {}
        },
        SET_CURRENT_USER (state, user) {
            state.currentUser = user
        }
    },

    actions: {
        async logoutUser ({ commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.mutate({
                    mutation: USER_LOGOUT
                })
                commit('LOGOUT_USER')
                return response.data.logout.ok
            } catch {
                return { error: 'Vous n’avez pas pu être déconnecté. Merci de réessayer.' }
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        },

        async loginUser ({ commit }, { username, password }) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.mutate({
                    mutation: USER_LOGIN,
                    variables: {
                        username,
                        password
                    }
                })

                const user = response.data.login.user
                commit('SET_CURRENT_USER', user)
                return response.data.login
            } catch {
                return { error: 'Nom d’utilisateur ou mot de passe incorrect. Merci de réessayer.' }
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        },

        /*
    This action get user with the sessionid cookie if the user is logged.
    */
        async loadUser ({ commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.query({
                    query: USER_CURRENT
                })
                commit('SET_CURRENT_USER', response.data.user)
            } catch {
                console.log('User not logged')
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        }
    },

    getters: {
        isSuperuser: (state) => state.currentUser.isSuperuser,
        findPermission: (state, getters) => {
            return (permissionName) => {
                let permission
                const splitPermission = permissionName.split('.')
                if (splitPermission.length === 2) {
                    permission = state.currentUser.userPermissions
                        .find(
                            permission =>
                                permission.codename === splitPermission[1] &&
                                permission.contentType.appLabel === splitPermission[0]
                        )
                } else {
                    permission = state.currentUser.userPermissions
                        .find(
                            permission => permission.codename === splitPermission[0])
                }
                return getters.isSuperuser || permission
            }
        },
        findGroup: (state, getters) => {
            return (groupName) =>
                getters.isSuperuser || state.currentUser.groups.find((group) => group === groupName)
        }
    }
}
