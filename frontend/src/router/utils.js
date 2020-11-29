import store from '@/store/index'

export async function loginRequired (to, _from) {
  if (store.state.auth.currentUser === null) {
    await store.dispatch('auth/loadUser')
  }

  const currentUser = store.state.auth.currentUser

  return !!(currentUser && currentUser.username)
}

export async function applicationPermissionRequired (
  to,
  _from,
  permission = 'members'
) {
  if (store.state.auth.currentUser === null) {
    await store.dispatch('auth/loadUser')
  }
  if (store.state.application.applications.length === 0) {
    await store.dispatch('application/getApplications')
  }

  const application = store.getters['application/applicationBySlug'](
    to.params.application
  )
  try {
    if (store.state.auth.currentUser.isSuperuser) {
      return true
    }
    if (
      application[permission].find(
        (user) => user.id === store.state.auth.currentUser.id
      )
    ) {
      return true
    } else {
      return false
    }
  } catch {
    return false
  }
}

export async function groupRequired (to, _from, groupRequired) {
  if (store.state.auth.currentUser === null) {
    await store.dispatch('auth/loadUser')
  }

  const currentUser = store.state.auth.currentUser

  if (currentUser && currentUser.username) {
    return !(
      !currentUser.isSuperuser &&
      currentUser.groups.filter((group) => group.name === groupRequired)
    )
  } else {
    return false
  }
}

export function utilsBeforeEach () {
  store.commit('START_LOADING')
}

export function utilsAfterEach () {
  store.commit('END_LOADING')
}
