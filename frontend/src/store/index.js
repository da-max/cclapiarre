import Vue from 'vue'
import Vuex from 'vuex'

import AuthModule from '@/store/utils/auth'
import AlertModule from '@/store/utils/alert'
import OrderModule from '@/store/application/order'
import ApplicationModule from '@/store/application/application'
import CoffeeModule from '@/store/coffee/coffee'
import CitrusModule from '@/store/citrus/citrus'
import CitrusOrderModule from '@/store/citrus/order'

Vue.use(Vuex)

export default new Vuex.Store({
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
        auth: AuthModule,
        alert: AlertModule,
        order: OrderModule,
        application: ApplicationModule,
        coffee: CoffeeModule,
        citrus: CitrusModule,
        citrusOrder: CitrusOrderModule
    }
})
