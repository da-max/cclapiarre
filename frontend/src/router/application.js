export default [
  {
    path: '/:application/commander',
    name: 'ApplicationOrder',
    component: () => import(/* webpackChunkName: "application-order" */ '../views/Application/Product/Order.vue'),
    props: route => ({ applicationSlug: route.params.application }),
    meta: { loginRequired: true, applicationPermission: 'members' }
  }
]
