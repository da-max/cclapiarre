<template>
  <div id="list-product">
    <loader v-show="loading"></loader>

    <div
      id="vue-messages"
      class="uk-width-2-5@m uk-width-3-4 uk-margin-auto uk-margin-xlarge-bottom"
    >
      <message v-show="queryError" :close="false" status="danger">
        <template #header>Erreur interne</template>
        <template #body>
          Une erreur est survenue, cela vient de nous, merci d'actualiser la
          page et de nous contacter si vous rencontrez de nouveau cette erreur.
        </template>
      </message>

      <message v-show="permissionError" :close="false" status="danger">
        <template #header>Accès interdit</template>
        <template #body
          >Il semblerait qui vous n’ayez pas l’autorisation d’accéder à cette
          fonctionnalité du site.</template
        >
      </message>

      <message
        v-for="message in messages"
        :key="message.id"
        :status="message.status"
      >
        <template #header>
          <div v-html="message.header"></div>
        </template>
        <template #body>
          <div v-html="message.body"></div>
        </template>
      </message>
    </div>
    <div class="uk-width-3-5@m uk-margin-auto">
      <div class="uk-margin-medium-bottom">
        <select
          name="actions"
          class="uk-select uk-form-width-medium"
          v-model="action"
        >
          <option value selected>------ ------</option>
          <option
            v-for="(name, value) in ACTIONS"
            :value="value"
            :key="value"
            >{{ name }}</option
          >
        </select>
        <input
          type="button"
          v-if="action !== ''"
          value="Appliquer"
          class="uk-button uk-button-primary uk-margin-medium-left"
          id="action-button"
          @click="applyAction()"
        />
      </div>

      <table
        class="uk-table uk-table-divider uk-striped uk-table-hover uk-table-middle"
      >
        <thead>
          <tr>
            <th class="uk-table-shrink">
              <input
                type="checkbox"
                class="uk-checkbox"
                title="Sélectionner tout les produits"
                v-model="checkAll"
              />
            </th>
            <th>Nom du produit</th>
            <th>
              <span
                uk-tooltip="Si le poids du produit est de 1, cela veut dire que le produit ne se vend pas au poids."
                >Poids du produit</span
              >
            </th>
            <th>Prix du produit</th>
            <th>
              <span
                uk-tooltip="Défini si ce produit est affiché, ou pas, sur le tableau des commandes."
                >Produit affiché</span
              >
            </th>
            <th>
              <span
                uk-tooltip="Permet d’afficher un message d’alerte sur le tableau de commande, afin de prévenir les adhérents que le produit sera, peut-être, pas disponible."
              >
                Produit peut être
                <br />non disponible
              </span>
            </th>
            <th class="uk-table-shrink">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>
              <input
                type="checkbox"
                class="uk-checkbox"
                v-model="product.check"
              />
            </td>
            <td>
              <drop pos="right">
                <template #button>{{ product.name }}</template>
                <template #header>{{ product.name }}</template>
                <template #body>
                  Prix : {{ product.price }} €
                  <br />
                  <span v-if="product.weight !== 1"
                    >Poids: {{ product.weight }} kg</span
                  >
                  <span v-else>Vendu à l’unité (poids : 1)</span>
                  <div v-html="product.description"></div>
                </template>
              </drop>
            </td>
            <td v-if="product.weight === 1">Vendu à l’unité</td>
            <td v-else>{{ product.weight }} kg</td>
            <td>{{ product.price }} €</td>
            <td v-if="product.display == true">
              <span uk-icon="check"></span>
            </td>
            <td v-else>
              <span uk-icon="close"></span>
            </td>
            <td v-if="product.maybeNotAvailable === true">
              <span uk-icon="check"></span>
            </td>
            <td v-else>
              <span uk-icon="close"></span>
            </td>
            <td>
              <modal :id="'confirm-delete-' + product.id">
                <template #header>
                  <h3>Supprimer {{ product.name }} ?</h3>
                </template>
                <template #body>
                  Vous êtes sur le point de supprimer le produit :
                  {{ product.name }},
                  <span class="uk-text-bold"
                    >il est recommandé de cacher le produit plutôt que de le
                    supprimer.</span
                  >
                </template>
                <template #footer>
                  <button
                    class="uk-button uk-button-danger"
                    @click.prevent="deleteProduct(product.id)"
                  >
                    Supprimer le produit
                  </button>
                  <button
                    class="uk-button uk-button-default uk-modal-close uk-margin-medium-left"
                  >
                    Annuler
                  </button>
                </template>
              </modal>
              <a
                :href="'/agrumes/modifier-un-produit/' + product.id"
                :title="'Modifier le produit : ' + product.name"
                uk-icon="icon: refresh; ratio: 1.20"
                class="uk-margin-small-right uk-icon-link"
              ></a>
              <a
                :uk-toggle="'target: #confirm_delete_' + product.id"
                :title="'Supprimer le produit : ' + product.name"
                uk-icon="icon: trash; ratio: 1.20"
              ></a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import Loader from '../utility/Loader';
import Message from '../utility/Message';
import Modal from '../utility/Modal';
import Drop from '../utility/Drop';

export default {
  name: 'ListProduct',

  data() {
    return {
      // Utility
      loading: false,
      queryError: false,
      permissionError: false,
      messages: Array(),

      products: Array(),
      action: String(),

      ACTIONS: {
        maybeNotAvailable: 'Produit potentiellement indisponible',
        available: 'Produit disponible',
        hide: 'Cacher ces produits',
        show: 'Afficher ces produits'
      }
    };
  },

  components: {
    Loader,
    Message,
    Modal,
    Drop
  },

  computed: {
    checkAll: {
      get() {
        return false;
      },
      set(value) {
        this.products.forEach(product => {
          product.check = value;
        });
      }
    }
  },

  methods: {
    async applyAction() {
      if (this.products.find(product => product.check === true) === undefined) {
        UIkit.notification(
          'Aucun produit sélctionné. <br>L’action ne peut être appliquée.',
          { status: 'warning', pos: 'bottom-right' }
        );
      } else {
        let productsCheck = this.products.filter(
          product => product.check === true
        );
        if (this.action === 'hide') {
          productsCheck = productsCheck.filter(product => {
            return product.display == true;
          });

          await productsCheck.forEach(product => {
            product.display = false;
          });
        } else if (this.action === 'show') {
          productsCheck = productsCheck.filter(product => {
            return product.display == false;
          });

          await productsCheck.forEach(product => {
            product.display = true;
          });
        } else if (this.action === 'maybeNotAvailable') {
          productsCheck = productsCheck.filter(product => {
            return product.maybeNotAvailable == false;
          });

          await productsCheck.forEach(product => {
            product.maybeNotAvailable = true;
          });
        } else if (this.action === 'available') {
          productsCheck = productsCheck.filter(product => {
            return product.maybeNotAvailable == true;
          });

          await productsCheck.forEach(product => {
            product.maybeNotAvailable = false;
          });
        }

        await productsCheck.forEach(product => {
          this.$product.update({ id: product.id }, product).then(
            response => {
              console.log(response);
              if (response.status !== 200) {
                this.queryError = true;
              }
            },
            response => {
              if (
                response.status === 403 &&
                response.statusText === 'Forbidden'
              ) {
                this.permissionError = true;
              } else {
                this.queryError = true;
              }
            }
          );
        });

        if ((this.queryError || this.permissionError) !== true) {
          this.messages.push({
            id: parseInt(Math.random() * 1000),
            status: 'success',
            header: 'Produits modifiés',
            body: 'Les produits sélectionnés ont bien été modifiés.'
          });
        }

        this.getProducts();
      }
    },

    getProducts() {
      this.$product.query().then(
        response => {
          response.body.forEach(product => {
            product.check = false;
          });
          this.products = response.body;
        },
        response => {
          if (response.statusText === 'Forbidden' && response.status === 403) {
            this.permissionError = true;
          } else {
            this.queryError = true;
          }
        }
      );
    },

    async deleteProduct(productId) {
      UIkit.modal('#confirm-delete-' + productId).hide();
      await this.$product.delete({ id: productId }).then(
        response => {
          this.messages.push({
            id: parseInt(Math.round() * 1000),
            header: 'Produit supprimé',
            body: 'Le produit a bien été supprimé.',
            status: 'success'
          });
        },
        response => {
          if (response.status === 400) {
            this.messages.push({
              id: parseInt(Math.round() * 1000),
              header: 'Erreur',
              bdoy:
                'Une erreur est survenue, le produit n’a pas pu être supprimé, merci d’actualiser la page, puis réessayer.',
              status: 'danger'
            });
          } else if (
            response.status === 403 &&
            response.statusText === 'Frobidden'
          ) {
            this.permissionError = true;
          } else {
            this.queryError = true;
          }
        }
      );
      this.getProducts();
      UIkit.scroll('', { offset: 150 }).scrollTo('#vue-messages');
    }
  },

  mounted() {
    this.$product = this.$resource(
      'api/citrus/product{/id}',
      { query: 'all' },
      {},
      {
        before: () => {
          this.loading = true;
        },

        after: () => {
          this.loading = false;
        }
      }
    );

    this.getProducts();
  }
};
</script>
