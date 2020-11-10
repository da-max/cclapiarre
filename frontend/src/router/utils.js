import store from '@/store/index'

const CONNECTION_URL = '/compte/connexion'

export async function loginRequired (to, _from, next) {
  if (store.state.auth.currentUser === null) {
    await store.dispatch('auth/loadUser')
  }

  const currentUser = store.state.auth.currentUser

  currentUser && currentUser.username ? next() : next(`${CONNECTION_URL}?next=${to.path}`)
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
