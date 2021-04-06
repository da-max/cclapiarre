import { computed } from '@vue/composition-api'

import { useShowModal, useHideModal } from '@/composition/useUtils'
import store from '@/store/index'

export default function () {
    // store state
    const carousels = computed(() => store.state.carousel.carousels)

    // Store getters
    const getCarouselById = (carouselId) => store.getters['carousel/getCarouselById'](carouselId)

    // Store mutations
    const setCarouselSelect = (carouselId) => { store.commit('carousel/SET_CAROUSEL_SELECT', carouselId) }
    const setCarouselSelectDefault = () => { store.commit('carousel/SET_CAROUSEL_SELECT_DEFAULT') }

    // store actions
    const deleteCarousel = () => {
        store.dispatch('carousel/deleteCarousel')
    }
    const getCarousels = async (force = false) => {
        await store.dispatch('carousel/getCarousels', force)
    }

    // State

    // Permissions
    const canAddCarousel = computed(() => store.getters['auth/findPermission']('carousel.add_carousel'))
    const canChangeCarousel = computed(() => store.getters['auth/findPermission']('carousel.change_carousel'))
    const canDeleteCarousel = computed(() => store.getters['auth/findPermission']('carousel.delete_carousel'))

    const carousel = computed(() => store.state.carousel.carouselSelect)

    // Methods

    const closeDeleteCarouselModal = () => {
        setCarouselSelectDefault()
        useHideModal('#carousel-delete-modal')
    }

    const saveCarousel = () => {
        useHideModal('#carousel-modal')
        if (carousel.value.id) {
            store.dispatch('carousel/updateCarousel')
        } else {
            store.dispatch('carousel/saveCarousel')
        }
    }

    const setCarousel = (carouselId) => {
        if (carouselId) {
            setCarouselSelect({ ...getCarouselById(carouselId) })
        } else {
            setCarouselSelectDefault()
        }
    }

    const showCarouselModal = (carouselId = undefined) => {
        setCarousel(carouselId)
        useShowModal('#carousel-modal')
    }

    const showDeleteCarouselModal = (carouselId) => {
        setCarousel(carouselId)
        useShowModal('#carousel-delete-modal')
    }

    const updateDescription = (e) => {
        setCarouselSelect({ ...carousel.value, description: e })
    }
    const updateImage = (e) => {
        setCarouselSelect({ ...carousel.value, image: e.target.files[0] })
    }
    const updatePosition = (e) => {
        setCarouselSelect({ ...carousel.value, position: e })
    }
    const updateTitle = (e) => {
        setCarouselSelect({ ...carousel.value, title: e })
    }

    return {
        // Store state
        carousel,
        carousels,

        // Store getters
        getCarouselById,

        // Store actions
        deleteCarousel,
        getCarousels,

        // Methods
        closeDeleteCarouselModal,
        saveCarousel,
        showCarouselModal,
        showDeleteCarouselModal,

        updateDescription,
        updateImage,
        updatePosition,
        updateTitle,

        // State
        canAddCarousel,
        canChangeCarousel,
        canDeleteCarousel
    }
}
