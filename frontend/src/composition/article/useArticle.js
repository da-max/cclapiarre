import { computed } from '@vue/composition-api'

import { useShowModal, useHideModal } from '@/composition/useUtils'
import store from '@/store/index'

export default function () {
    // Store state
    const articles = computed(() => store.state.article.articles)

    // Store getters
    const getArticleSelect = computed(() => store.getters['article/getArticleSelect'])

    // Store mutations
    const setArticleSelect = (articleId) => { store.commit('article/SET_ARTICLE_SELECT', articleId) }

    // Store actions
    const getArticles = () => { store.dispatch('article/getArticles') }

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
            categoryId: 0
        })

    const canChangeArticle = computed(() => store.getters['auth/findPermission']('article.change_article'))
    const canDeleteArticle = computed(() => store.getters['auth/findPermission']('article.delete_article'))

    return {
        // Store state
        articles,

        // Store getters
        getArticleSelect,

        // Store actions
        getArticles,

        // State
        article,

        // Methods
        canChangeArticle,
        canDeleteArticle,
        closeArticleModal,
        showArticleModal
    }
}
