import apolloClient from '@/vue-apollo'

import ARTICLE_ALL from '@/graphql/Article/ArticleAll.gql'
import CATEGORY_ALL from '@/graphql/Article/Category/CategoryAll.gql'
import ARTICLE_ADD from '@/graphql/Article/ArticleAdd.gql'

export default {
    namespaced: true,
    state: () => ({
        articles: [],
        articleSelect: {
            title: '',
            content: '',
            category: null
        },
        categories: []
    }),
    mutations: {
        ADD_ARTICLE (state, article) {
            state.articles = [article, ...state.articles]
        },

        SET_ARTICLE_SELECT (state, article) {
            state.articleSelect = article
        },

        SET_ARTICLE_SELECT_DEFAULT (state) {
            state.articleSelect = {
                title: '',
                content: '',
                category: null
            }
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
        },

        async saveArticle ({ state, commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.mutate({
                    mutation: ARTICLE_ADD,
                    variables: {
                        input: state.articleSelect
                    }
                })

                commit('ADD_ARTICLE', { ...response.data.addArticle.article })
                commit('alert/ADD_ALERT', {
                    header: false,
                    body: 'L’article a bien été ajouté.',
                    status: 'success',
                    close: true
                }, { root: true })
            } catch (e) {
                commit('alert/ADD_ERROR', e, { root: true })
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        },

        async updateArticle ({ state, commit }) {
        }
    },
    getters: {
        getArticleSelect: (state) =>
            state.articles.find(article => article.id === state.articleSelect)
    }
}
