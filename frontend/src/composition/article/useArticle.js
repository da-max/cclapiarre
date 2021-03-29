import { computed } from '@vue/composition-api'

import { useShowModal, useHideModal } from '@/composition/useUtils'
import store from '@/store/index'

export default function () {
    // Store state
    const articles = computed(() => store.state.article.articles)
    const categories = computed(() => store.state.article.categories)

    // Store getters
    const getArticleSelect = computed(() => store.getters['article/getArticleSelect'])

    // Store mutations
    const setArticleSelect = (articleId) => { store.commit('article/SET_ARTICLE_SELECT', articleId) }

    // Store actions
    const getArticles = () => { store.dispatch('article/getArticles') }
    const getCategories = () => { store.dispatch('article/getCategories') }

    // Methods
    const closeArticleModal = async () => {
        setArticleSelect(undefined)
        useHideModal('#article-modal')
    }

    const showArticleModal = async (articleId = undefined) => {
        setArticleSelect(articleId)
        useShowModal('#article-modal')
    }

    // State
    const article = computed(() => getArticleSelect.value !== undefined
        ? { ...getArticleSelect.value } : {
            title: '',
            content: '',
            category: {
                id: null
            }
        })

    const canAddArticle = computed(() => store.getters['auth/findPermission']('article.add_article'))
    const canChangeArticle = computed(() => store.getters['auth/findPermission']('article.change_article'))
    const canDeleteArticle = computed(() => store.getters['auth/findPermission']('article.delete_article'))

    return {
        // Store state
        articles,
        categories,

        // Store getters
        getArticleSelect,

        // Store actions
        getArticles,
        getCategories,

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
