import store from '@/store/index'

const CONNECTION_URL = '/compte/connexion'

export async function loginRequired (to, _from, next) {
  if (store.state.auth.currentUser === null) {
    await store.dispatch('auth/loadUser')
  }
  const currentUser = store.state.auth.currentUser

  currentUser && currentUser.username ? next() : next(`${CONNECTION_URL}?next=${to.path}`)
}

export async function applicationPermissionRequired (to, _from, next, permission = 'admins') {
  if (store.state.auth.currentUser === null) {
    await store.dispatch('auth/loadUser')
  }
  if (store.state.application.applications.length === 0) {
    await store.dispatch('application/getApplications')
  }

  const application = store.getters['application/applicationBySlug'](to.params.application)
  if (application[permission].find(user => user.id === store.state.auth.currentUser.id)) { next() } else {
    store.commit('alert/ADD_ALERT', {
      header: true,
      headerContent: 'Accès refusé !',
      body: 'Vous n’avez pas la permission d’accéder à cette page.',
      status: 'danger',
      close: true
    })
    next(`${CONNECTION_URL}?next=${to.path}`)
  }
}

export async function groupRequired (to, _from, next, groupRequired) {
  if (store.state.auth.currentUser === null) {
    await store.dispatch('auth/loadUser')
  }

  const currentUser = store.state.auth.currentUser

  if (currentUser && currentUser.username) {
    !currentUser.isSuperuser && currentUser.groups.filter(group => group.name === groupRequired)
      ? next(`${CONNECTION_URL}?next=${to.path}`)
      : next()
  } else {
    next(`${CONNECTION_URL}?next=${to.path}`)
  }
}

export function utilsBeforeEach () {
  store.commit('START_LOADING')
}

export function utilsAfterEach () {
  store.commit('END_LOADING')
}
