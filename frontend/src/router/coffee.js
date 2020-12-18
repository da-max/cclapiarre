export default [
  {
    path: '/cafe/commander',
    name: 'CoffeeOrder',
    component: () => import(/* webpackChunkName: "coffee-order" */ '../views/Coffee/Order.vue'),
    meta: { loginRequired: true }
  }
]
