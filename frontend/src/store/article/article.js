import apolloClient from '@/vue-apollo'

import ARTICLE_ALL from '@/graphql/Article/ArticleAll.gql'
import CATEGORY_ALL from '@/graphql/Article/Category/CategoryAll.gql'

export default {
    namespaced: true,
    state: () => ({
        articles: [],
        articleSelect: null,
        categories: []
    }),
    mutations: {
        SET_ARTICLE_SELECT (state, articleId) {
            state.articleSelect = articleId
        },
        SET_ARTICLES (state, articles) {
            state.articles = articles
        },

        SET_CATEGORIES (state, categories) {
            state.categories = categories
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
                commit('alert/ADD_ERROR', e, { root: true })
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        },

        async getCategories ({ commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.query({
                    query: CATEGORY_ALL
                })
                commit('SET_CATEGORIES', response.data.allCategories)
            } catch (e) {
                commit('alert/ADD_ERROR', e, { root: true })
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
