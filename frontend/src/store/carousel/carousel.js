import apolloClient from '@/vue-apollo'

import CAROUSEL_ADD from '@/graphql/Carousel/CarouselAdd.gql'
import CAROUSEL_ALL from '@/graphql/Carousel/CarouselAll.gql'
import CAROUSEL_DELETE from '@/graphql/Carousel/CarouselDelete.gql'
import CAROUSEL_UPDATE from '@/graphql/Carousel/CarouselUpdate.gql'

export default {
    namespaced: true,
    state: () => ({
        carousels: [],
        carouselSelect: {
            title: '',
            description: '',
            position: 47,
            image: {}
        }
    }),
    mutations: {
        ADD_CAROUSEL (state, carousel) {
            const carousels = [...state.carousels, carousel]
            state.carousels = carousels.sort((a, b) => a.position > b.position ? 1 : -1)
        },

        DELETE_CAROUSEL (state, carouselId) {
            state.carousels = state.carousels.filter(c => c.id !== carouselId)
        },

        SET_CAROUSELS (state, carousels) {
            state.carousels = [...carousels].sort((a, b) => a.position > b.position ? 1 : -1)
        },

        SET_CAROUSEL_SELECT (state, carousel) {
            state.carouselSelect = carousel
        },

        SET_CAROUSEL_SELECT_DEFAULT (state) {
            state.carouselSelect = {
                title: '',
                description: '',
                position: 47,
                image: {}
            }
        },

        UPDATE_CAROUSEL (state, carousel) {
            state.carousels = [
                carousel,
                ...state.carousels.filter(c => c.id !== carousel.id)

            ]
        }
    },
    actions: {
        async deleteCarousel ({ state, commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.mutate({
                    mutation: CAROUSEL_DELETE,
                    variables: { id: state.carouselSelect.id }
                })
                commit('DELETE_CAROUSEL', response.data.deleteCarousel.deletedId)
                commit('alert/ADD_ALERT', {
                    header: false,
                    body: 'Le carousel a bien été supprimé.',
                    status: 'success',
                    close: true
                }, { root: true })
            } catch (e) {
                commit('alert/ADD_ERROR', e, { root: true })
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        },

        async getCarousels ({ state, commit }, force = false) {
            if (state.carousels.length === 0 || force) {
                commit('START_LOADING', null, { root: true })
                try {
                    const response = await apolloClient.query({
                        query: CAROUSEL_ALL
                    })
                    commit('SET_CAROUSELS', response.data.allCarousels)
                } catch (e) {
                    console.log(e)
                    commit('alert/ADD_ERROR', e, { root: true })
                } finally {
                    commit('END_LOADING', null, { root: true })
                }
            }
        },

        async saveCarousel ({ state, commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const response = await apolloClient.mutate({
                    mutation: CAROUSEL_ADD,
                    variables: { input: state.carouselSelect }
                })
                commit('alert/ADD_ALERT', {
                    header: false,
                    body: 'Le carousel a bien été ajouté !',
                    status: 'success',
                    close: true
                }, { root: true })
                commit('ADD_CAROUSEL', response.data.addCarousel.carousel)
            } catch (e) {
                commit('alert/ADD_ERROR', e, { root: true })
            } finally {
                commit('END_LOADING', null, { root: true })
            }
        },

        async updateCarousel ({ state, commit }) {
            commit('START_LOADING', null, { root: true })
            try {
                const carousel = {
                    title: state.carouselSelect.title,
                    description: state.carouselSelect.description,
                    image: state.carouselSelect.image,
                    position: state.carouselSelect.position
                }
                const response = await apolloClient.mutate({
                    mutation: CAROUSEL_UPDATE,
                    variables: {
                        id: state.carouselSelect.id,
                        input: carousel
                    }
                })
                commit('UPDATE_CAROUSEL', { ...response.data.updateCarousel.carousel })

                commit('alert/ADD_ALERT', {
                    header: false,
                    body: 'Le carousel a bien été modifié !',
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
        getCarouselById: (state) => {
            return (carouselId) => state.carousels.find(
                c => c.id === carouselId
            )
        }
    }
}
