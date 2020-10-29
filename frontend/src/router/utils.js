import store from '@/store/index'

export function loginRequired (to, _from, next) {
  const currentUser = store.state.auth.currentUser

  currentUser && currentUser.username ? next() : next(`/compte/connexion?next=${to.path}`)
}

export function groupRequired (to, _from, next, groupRequired) {
  loginRequired(to, _from, next)
  const currentUser = store.state.auth.currentUser

  !currentUser.isSuperuser && currentUser.groups.filter(group => group.name === groupRequired)
    ? next(`/compte/connexion?next=${to.path}`)
    : next()
}
