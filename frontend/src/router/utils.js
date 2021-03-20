import store from '@/store/index'

export async function loginRequired (to, _from) {
    if (store.state.auth.currentUser === null) {
        await store.dispatch('auth/loadUser')
    }
    return !!(store.state.auth.currentUser && store.state.auth.currentUser.username)
}

export async function applicationPermissionRequired (
    to,
    from,
    permission = 'admins'
) {
    let hasPermission
    if (loginRequired(to, from)) {
        if (store.state.application.applications.length === 0) {
            await store.dispatch('application/getApplications')
            const application = store
                .getters['application/applicationBySlug'](to.params.application)
            hasPermission = application[permission].find(
                (user) => user.id === store.state.auth.currentUser.id
            )
        }
        if (!hasPermission) {
            store.commit('alert/ADD_PERMISSION_DENIED')
        }
    }
    return !!hasPermission
}

export async function groupRequired (to, from, groupRequired) {
    let group
    if (loginRequired(to, from)) {
        group = store.getters['auth/findGroup'](groupRequired)
    }
    return !!group
}

export function permissionRequired (to, from, permission) {
    let hasPermission
    if (loginRequired(to, from)) {
        hasPermission = store.getters['auth/findPermission'](permission)
    }
    return !!hasPermission
}

export function utilsBeforeEach () {
    store.commit('START_LOADING')
}

export function utilsAfterEach () {
    store.commit('END_LOADING')
}
