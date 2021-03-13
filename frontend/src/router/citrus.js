export default [
    {
        path: '/agrumes/liste-des-produits',
        name: 'CitrusList',
        component: () => import(/* webpackChunkName "citrus-list" */'../views/Citrus/ProductList.vue'),
        meta: { loginRequired: true }
    },
    {
        path: '/agrumes/commander',
        name: 'CitrusOrder',
        component: () => import(/* webpackChunkName "citrus-order" */'../views/Citrus/Order'),
        meta: { loginRequired: true }
    }
]
