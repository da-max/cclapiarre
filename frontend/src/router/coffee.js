export default [
  {
    path: '/cafe/commander',
    name: 'CoffeeOrder',
    component: () => import(/* webpackChunkName: "coffee-order" */ '../views/Coffee/Order.vue'),
    meta: { loginRequired: true }
  },
  {
    path: '/cafe/liste-des-commandes',
    name: 'CoffeeOrderList',
    component: () => import(/* webpackChunkName: "coffee-order-list" */ '../views/Coffee/OrderList.vue'),
    meta: { loginRequired: true }
  }
]
