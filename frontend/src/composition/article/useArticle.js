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
    const getArticles = () => { store.dispatch('article/getArticles') }
    const getCategories = () => { store.dispatch('article/getCategories') }
    const saveArticle = async () => { await store.dispatch('article/saveArticle') }
    const updateArticle = async () => { await store.dispatch('article/updateArticle') }

    // Methods
    const closeArticleModal = async () => {
        setArticleSelectDefault()
        useHideModal('#article-modal')
    }

    const showArticleModal = (articleId = undefined) => {
        if (articleId) {
            const article = getArticleById(articleId)
            setArticleSelect({
                ...article,
                category: article.category.id
            })
        } else {
            setArticleSelectDefault()
        }
        useShowModal('#article-modal')
    }

    // State

    const canAddArticle = computed(() => store.getters['auth/findPermission']('article.add_article'))
    const canChangeArticle = computed(() => store.getters['auth/findPermission']('article.change_article'))
    const canDeleteArticle = computed(() => store.getters['auth/findPermission']('article.delete_article'))

    return {
        // Store state
        articles,
        categories,

        // Store getters
        getArticleById,

        // Store actions
        getArticles,
        getCategories,
        saveArticle,
        updateArticle,

        // State
        article,

        // Methods
        canAddArticle,
        canChangeArticle,
        canDeleteArticle,

        closeArticleModal,
        showArticleModal
    }
}
