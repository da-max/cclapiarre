import { computed } from '@vue/composition-api'

import { useShowModal, useHideModal } from '@/composition/useUtils'
import store from '@/store/index'

export default function () {
    // Store state
    const article = computed(() => store.state.article.articleSelect)
    const articles = computed(() => store.state.article.articles)
    const categories = computed(() => store.state.article.categories)

    // Store getters
    const getArticleById = (articleId) => store.getters['article/getArticleById'](articleId)

    // Store mutations
    const setArticleSelect = (article) => { store.commit('article/SET_ARTICLE_SELECT', article) }
    const setArticleSelectDefault = () => { store.commit('article/SET_ARTICLE_SELECT_DEFAULT') }

    // Store actions
    const deleteArticle = () => { store.dispatch('article/deleteArticle') }
    const getArticles = () => { store.dispatch('article/getArticles') }
    const getCategories = () => { store.dispatch('article/getCategories') }
    const saveArticle = async () => { await store.dispatch('article/saveArticle') }
    const updateArticle = async () => { await store.dispatch('article/updateArticle') }

    // Methods
    const closeArticleModal = () => {
        setArticleSelectDefault()
        useHideModal('#article-modal')
    }

    const closeDeleteArticleModal = () => {
        setArticleSelectDefault()
        useHideModal('#article-delete-modal')
    }

    const setArticle = (articleId) => {
        if (articleId) {
            const article = getArticleById(articleId)
            setArticleSelect({
                ...article,
                category: article.category.id
            })
        } else {
            setArticleSelectDefault()
        }
    }

    const showArticleModal = (articleId = undefined) => {
        setArticle(articleId)
        useShowModal('#article-modal')
    }

    const showDeleteArticleModal = (articleId) => {
        setArticle(articleId)
        useShowModal('#article-delete-modal')
    }

    // State
    const canAddArticle = computed(() => store.getters['auth/findPermission']('article.add_article'))
    const canChangeArticle = computed(() => store.getters['auth/findPermission']('article.change_article'))
    const canDeleteArticle = computed(() => store.getters['auth/findPermission']('article.delete_article'))

    return {
        // Store state
        article,
        articles,
        categories,

        // Store getters
        getArticleById,

        // Store actions
        deleteArticle,
        getArticles,
        getCategories,
        saveArticle,
        updateArticle,

        // Methods
        canAddArticle,
        canChangeArticle,
        canDeleteArticle,

        closeArticleModal,
        closeDeleteArticleModal,
        showArticleModal,
        showDeleteArticleModal
    }
}
