export default [
    {
        path: '/carousel/liste-des-carousels',
        name: 'CarouselList',
        component: () => import(/* webpackChunkName "carousel-list" */'../views/Carousel/CarouselList.vue'),
        meta: {
            loginRequired: true,
            permissionRequired: 'carousel.view_carousel'
        }
    }
]
