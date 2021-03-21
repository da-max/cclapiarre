export default [
    {
        path: '/article/liste-des-articles',
        name: 'ArticleList',
        component: () => import(/* webpackChunkName "article-list" */'../views/Article/ArticleList.vue'),
        meta: {
            loginRequired: true,
            permissionRequired: 'article.view_article'
        }
    }
]
