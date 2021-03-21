import { computed } from '@vue/composition-api'
import { useResult } from '@vue/apollo-composable'

import { useUtilsQuery } from '@/composition/useUtils'
import store from '@/store/index'

import ARTICLE_ALL from '@/graphql/Article/ArticleAll.gql'

export default function () {
    const allArticle = () => {
        const { result, loading } = useUtilsQuery(ARTICLE_ALL)
        const articles = useResult(result)

        return {
            articles,
            loading
        }
    }

    const canChangeArticle = computed(() => store.getters['auth/findPermission']('article.change_article'))
    const canDeleteArticle = computed(() => store.getters['auth/findPermission']('article.delete_article'))

    return {
        allArticle,
        canChangeArticle,
        canDeleteArticle
    }
}
