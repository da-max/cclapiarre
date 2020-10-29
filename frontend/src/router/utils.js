import store from '@/store/index'

const CONNECTION_URL = '/compte/connexion'

export function loginRequired (to, _from, next) {
  const currentUser = store.state.auth.currentUser

  currentUser && currentUser.username ? next() : next(`${CONNECTION_URL}?next=${to.path}`)
}

export function groupRequired (to, _from, next, groupRequired) {
  const currentUser = store.state.auth.currentUser

  if (currentUser && currentUser.username) {
    !currentUser.isSuperuser && currentUser.groups.filter(group => group.name === groupRequired)
      ? next(`${CONNECTION_URL}?next=${to.path}`)
      : next()
  } else {
    next(`${CONNECTION_URL}?next=${to.path}`)
  }
}
