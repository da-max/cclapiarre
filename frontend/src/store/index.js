import Vue from 'vue'
import Vuex from 'vuex'

import AlertModule from '@/store/utils/alert'
import ApplicationModule from '@/store/application/application'
import ArticleModule from '@/store/article/article'
import AuthModule from '@/store/utils/auth'
import CarouselModule from '@/store/carousel/carousel'
import CitrusModule from '@/store/citrus/citrus'
import CitrusOrderModule from '@/store/citrus/order'
import CoffeeModule from '@/store/coffee/coffee'
import OrderModule from '@/store/application/order'

Vue.use(Vuex)

export default new Vuex.Store({
    strict: true,
    state: {
        loading: false
    },
    mutations: {
        START_LOADING (state) {
            state.loading = true
        },
        END_LOADING (state) {
            state.loading = false
        }
    },

    actions: {

    },
    modules: {
        alert: AlertModule,
        application: ApplicationModule,
        article: ArticleModule,
        auth: AuthModule,
        carousel: CarouselModule,
        citrus: CitrusModule,
        citrusOrder: CitrusOrderModule,
        coffee: CoffeeModule,
        order: OrderModule
    }
})
