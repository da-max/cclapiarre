import Vue from 'vue'
import { ApolloClient, InMemoryCache } from '@apollo/client/core'
import { createUploadLink } from 'apollo-upload-client'

// Name of the localStorage item
const AUTH_TOKEN = 'apollo-token'

// Http endpoint
const httpEndpoint = process.env.VUE_APP_GRAPHQL_HTTP || 'http://localhost:8000/graphql'
// Files URL root
export const filesRoot = process.env.VUE_APP_FILES_ROOT || httpEndpoint.substr(0, httpEndpoint.indexOf('/graphql'))

Vue.prototype.$filesRoot = filesRoot

// function getCookie (name) {
//   var cookieValue = null
//   if (document.cookie && document.cookie !== '') {
//     var cookies = document.cookie.split(';')
//     for (var i = 0; i < cookies.length; i++) {
//       var cookie = cookies[i].trim()
//       // Does this cookie string begin with the name we want?
//       if (cookie.substring(0, name.length + 1) === name + '=') {
//         cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
//         break
//       }
//     }
//   }
//   return cookieValue
// }

const httpUploadLink = createUploadLink({
    uri: httpEndpoint,
    tokenName: AUTH_TOKEN,
    persisting: false,
    websocketsOnly: false,
    ssr: false
})

// const httpLink = createHttpLink({
//   uri: httpEndpoint,
//   httpLinkOptions: {
//     headers: {
//       'X-CSRFToken': getCookie('csrftoken')
//     }
//   },
//   tokenName: AUTH_TOKEN,
//   persisting: false,
//   websocketsOnly: false,
//   ssr: false
// })

const cache = new InMemoryCache()

export function createClient (options = {}) {
    // Create apollo client
    const apolloClient = new ApolloClient({
        link: httpUploadLink,
        cache,
        ...options
    })

    return apolloClient
}

// // Call this in the Vue app file
// export function createProvider (options = {}) {
//   const apolloClient = createClient(options)
//
//   // Create vue apollo provider
//   const apolloProvider = new VueApollo({
//     defaultClient: apolloClient,
//     defaultOptions: {
//       $query: {
//         // fetchPolicy: 'cache-and-network',
//       }
//     },
//     errorHandler (error) {
//       // eslint-disable-next-line no-console
//       console.log('%cError', 'background: red; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;', error.message)
//     }
//   })
//
//   return apolloProvider
// }
//
// // Manually call this when user log in
// export async function onLogin (apolloClient, token) {
//   if (typeof localStorage !== 'undefined' && token) {
//     localStorage.setItem(AUTH_TOKEN, token)
//   }
//   if (apolloClient.wsClient) restartWebsockets(apolloClient.wsClient)
//   try {
//     await apolloClient.resetStore()
//   } catch (e) {
//     // eslint-disable-next-line no-console
//     console.log('%cError on cache reset (login)', 'color: orange;', e.message)
//   }
// }
//
// // Manually call this when user log out
// export async function onLogout (apolloClient) {
//   if (typeof localStorage !== 'undefined') {
//     localStorage.removeItem(AUTH_TOKEN)
//   }
//   if (apolloClient.wsClient) restartWebsockets(apolloClient.wsClient)
//   try {
//     await apolloClient.resetStore()
//   } catch (e) {
//     // eslint-disable-next-line no-console
//     console.log('%cError on cache reset (logout)', 'color: orange;', e.message)
//   }
// }
//
const apolloClient = createClient()

export default apolloClient
