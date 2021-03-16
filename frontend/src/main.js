import Vue from 'vue'
import VueComp, { provide } from '@vue/composition-api'
import { DefaultApolloClient } from '@vue/apollo-composable'
import App from './App.vue'
import router from './router'
import store from './store'
import apolloClient from './vue-apollo'
import UIkit from 'uikit'
import '@/assets/styles/styles.scss'
import Icons from 'uikit/dist/js/uikit-icons'

UIkit.use(Icons)
window.UIkit = UIkit

Vue.config.productionTip = false

Vue.use(VueComp)

new Vue({
    setup () {
        provide(DefaultApolloClient, apolloClient)
    },
    router,
    store,
    render: h => h(App)
}).$mount('#app')
