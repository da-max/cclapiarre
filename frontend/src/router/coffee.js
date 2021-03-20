export default [
    {
        path: '/cafe/commander',
        name: 'CoffeeOrder',
        component: () => import(/* webpackChunkName: "coffee-order" */ '../views/Coffee/Order.vue'),
        meta: {
            loginRequired: true,
            permissionsRequired: ['coffee.view_coffee', 'coffee.add_coffeeorder']
        }
    },
    {
        path: '/cafe/liste-des-commandes',
        name: 'CoffeeOrderList',
        component: () => import(/* webpackChunkName: "coffee-order-list" */ '../views/Coffee/OrderList.vue'),
        meta: {
            loginRequired: true,
            permissionRequired: 'coffee.view_coffeeorder'
        }
    }
]
