import apolloClient from '@/vue-apollo'

import ARTICLE_ALL from '@/graphql/Article/ArticleAll.gql'

export default {
    namespaced: true,
    state: () => ({
        articles: [],
        articleSelect: '1'
    }),
    mutations: {
        SET_ARTICLE_SELECT (state, articleId) {
            state.articleSelect = articleId
        },
        SET_ARTICLES (state, articles) {
            state.articles = articles
        }
    },
    actions: {
        async getArticles ({ commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.query({
                    query: ARTICLE_ALL
                })
                commit('SET_ARTICLES', response.data.allArticles)
            } catch (e) {
                commit('alert/ADD_ALERT', {
                    header: false,
                    body: `Une erreur est survenue, merci de réessayer : ${e}`,
                    status: 'danger',
                    close: true
                }, { root: true })
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        }
    },
    getters: {
        getArticleSelect: (state) =>
            state.articles.find(article => article.id === state.articleSelect)
    }
}
