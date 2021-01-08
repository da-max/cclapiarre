export default [
  {
    path: '/agrumes/liste-des-produits',
    name: 'CitrusList',
    component: () => import(/* webpackChunkName "citrus-list" */'../views/Citrus/ProductList.vue'),
    meta: { loginRequired: true }
  }
]
