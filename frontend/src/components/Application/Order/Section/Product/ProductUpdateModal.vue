<template>
  <UtilsModal
    v-if="!loading"
    :container="true"
    :center="true"
    :esc-close="false"
  >
    <template #header>
      <h2 class="uk-modal-title">
        Modifier le produit : {{ productUpdated.name }}
      </h2>
    </template>
    <template #body>
      <form class="">
        <div class="uk-child-width-1-2@l uk-grid-medium uk-flex-center" uk-grid>
          <FormInput
            type="text"
            name="name"
            label="Nom du produit"
            :value="productUpdated.name"
            v-model="productUpdated.name"
          />
          <fieldset class="uk-fieldset uk-text-center">
            <legend class="uk-legend uk-margin-small-bottom">
              Options du produit
            </legend>
            <div class="uk-inline">
              <button
                type="button"
                uk-icon="plus"
                class="uk-icon-button"
                title="Créer une option"
              ></button>
              <UtilsDrop pos="left" id="addOption">
                <template>
                  <FormInput
                    style="z-index: 999"
                    type="text"
                    :value="newOption"
                    v-model="newOption"
                    name="option-name"
                    label="Nom de l’option"
                  />
                  <UtilsButton
                    width="small"
                    @click="addOption($route.params.application)"
                    >Créer l’option</UtilsButton
                  >
                </template>
              </UtilsDrop>
            </div>
            <div class="uk-height-small uk-overflow-auto">
              <div v-for="option in options.edges" :key="option.node.id">
                <label :for="option.node.id" class="uk-form-label">{{
                  option.node.name
                }}</label>
                <div class="uk-form-controls">
                  <input
                    :checked="optionSelected(option.node.id)"
                    type="checkbox"
                    :name="option.node.id"
                    class="uk-checkbox"
                  />
                </div>
              </div>
            </div>
          </fieldset>
        </div>
        <div
          class="uk-child-width-1-4@l uk-child-width-1-2@m uk-grid-medium uk-flex-center"
          uk-grid
        >
          <div>
            <div uk-form-custom>
              <input type="file" />
              <button
                class="uk-button uk-button-default"
                type="button"
                tabindex="-1"
              >
                Image du produit
              </button>
            </div>
            <p class="uk-text-muted">Cette image sera affiché sur la page des commandes.</p>
          </div>
          <div>
            <label for="display" class="uk-form-label"
              >Afficher le produit</label
            >
            <div class="uk-form-controls">
              <input
                type="checkbox"
                name="display"
                v-model="productUpdated.display"
                class="uk-checkbox"
              />
            </div>
            <p class="uk-text-muted">
              Si cette case est décochée, le produit sera caché et ne sera pas
              commandable.
            </p>
          </div>
          <div>
            <FormInput
              :value="productUpdated.maximum"
              :v-model="productUpdated.maximum"
              type="number"
              name="maximum"
              label="Maximum par commande"
            />
            <p class="uk-text-muted">
              Défini la quantité maximale commandable par adhérent.
            </p>
          </div>
          <div>
            <FormInput
              :value="productUpdated.maximumAll"
              v-model="productUpdated.maximumAll"
              type="number"
              name="maximum-all"
              label="Maximum pour le produit"
            />
            <p class="uk-text-muted">
              Défini la quantité maximal commandable par tout les adhérents.
            </p>
          </div>
        </div>
      </form>
    </template>
  </UtilsModal>
</template>

<script>
import { computed } from '@vue/composition-api'

import store from '@/store/index'

import useOption from '@/composition/application/product/useOption'
import { useUtilsMutation } from '@/composition/useUtils'

import UtilsModal from '@/components/Utils/UtilsModal'
import UtilsDrop from '@/components/Utils/UtilsDrop'
import FormInput from '@/components/Utils/Form/FormInput'
import UtilsButton from '@/components/Utils/UtilsButton.vue'

export default {
  name: 'ProductUpdateModal',
  setup (props, ctx) {
    // Computed
    // ==========
    const productUpdated = computed(() => ({ ...props.product }))

    const optionSelected = (optionId) =>
      !!productUpdated.value.options.edges.find(
        (option) => option.node.id === optionId
      )

    const {
      options,
      newOption,
      loading,
      getOptionsByApplicationSlug,
      optionAdd
    } = useOption()

    getOptionsByApplicationSlug((ctx) => ({
      applicationSlug: ctx.$route.params.application
    }))

    const addOption = (applicationSlug) => {
      const input = {
        name: newOption.value,
        application: store.getters['application/idApplicationBySlug'](applicationSlug)
      }
      useUtilsMutation(optionAdd, input)
    }

    return {
      options,
      loading,
      productUpdated,
      optionSelected,
      newOption,
      addOption
    }
  },
  props: {
    product: {
      required: true,
      type: Object
    }
  },
  components: {
    UtilsModal,
    FormInput,
    UtilsDrop,
    UtilsButton
  }
}
</script>
