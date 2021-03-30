import apolloClient from '@/vue-apollo'

import ARTICLE_ADD from '@/graphql/Article/ArticleAdd.gql'
import ARTICLE_ALL from '@/graphql/Article/ArticleAll.gql'
import ARTICLE_DELETE from '@/graphql/Article/ArticleDelete.gql'
import ARTICLE_UPDATE from '@/graphql/Article/ArticleUpdate.gql'
import CATEGORY_ALL from '@/graphql/Article/Category/CategoryAll.gql'

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

        DELETE_ARTICLE (state, articleId) {
            state.articles = state.articles.filter(a => a.id !== articleId)
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
        },

        UPDATE_ARTICLE (state, article) {
            state.articles = [
                article,
                ...state.articles.filter(a => a.id !== article.id)
            ]
        }
    },
    actions: {
        async deleteArticle ({ state, commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.mutate({
                    mutation: ARTICLE_DELETE,
                    variables: {
                        id: state.articleSelect.id
                    }
                })

                commit('DELETE_ARTICLE', response.data.deleteArticle.deletedId)
                commit('alert/ADD_ALERT', {
                    header: false,
                    body: 'L’article a bien été supprimé.',
                    status: 'success',
                    close: true
                }, { root: true })
            } catch (e) {
                commit('alert/ADD_ERROR', e, { root: true })
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        },

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
            commit('START_LOADING', null, { root: true })
            try {
                const article = {
                    title: state.articleSelect.title,
                    content: state.articleSelect.content,
                    category: state.articleSelect.category
                }
                const response = await apolloClient.mutate({
                    mutation: ARTICLE_UPDATE,
                    variables: {
                        id: state.articleSelect.id,
                        input: article
                    }
                })

                commit('UPDATE_ARTICLE', { ...response.data.updateArticle.article })
                commit('alert/ADD_ALERT', {
                    header: false,
                    body: 'L’article a bien été modifié.',
                    status: 'success',
                    close: true
                }, { root: true })
            } catch (e) {
                commit('alert/ADD_ERROR', e, { root: true })
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        }
    },
    getters: {
        getArticleById: (state) => {
            return (articleId) => state.articles.find(article => article.id === articleId)
        }
    }
}
