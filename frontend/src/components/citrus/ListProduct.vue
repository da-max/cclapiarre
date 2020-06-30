<template>
  <div id="list-product">
    <loader v-show="loading"></loader>

    <div
      id="vue-messages"
      class="uk-width-2-5@m uk-width-3-4 uk-margin-auto uk-margin-xlarge-bottom"
    >
      <message v-show="query_error" :close="false" status="danger">
        <template #header>Erreur interne</template>
        <template #body>
          Une erreur est survenue, cela vient de nous, merci d'actualiser la
          page et de nous contacter si vous rencontrez de nouveau cette erreur.
        </template>
      </message>

      <message v-show="permission_error" :close="false" status="danger">
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
          @click="apply_action()"
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
                title="Sélectionner tous les produits"
                v-model="check_all"
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
                uk-tooltip="Permet d’afficher un message d’alerte sur le tableau de commande, afin de prévenir les adhérents que le produit sera, peut être, pas disponible."
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
            <td v-if="product.maybe_not_available == true">
              <span uk-icon="check"></span>
            </td>
            <td v-else>
              <span uk-icon="close"></span>
            </td>
            <td>
              <modal :id="'confirm_delete_' + product.id">
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
                    @click.prevent="delete_product(product.id)"
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
      <div class="uk-text-center uk-margin-large-top">
        <button
          class="uk-button uk-button-default"
          type="button"
          @click="get_more_product()"
          v-show="display_button_get_more_product"
        >
          Afficher plus de produit
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Loader from "../utility/Loader";
import Message from "../utility/Message";
import Modal from "../utility/Modal";
import Drop from "../utility/Drop";

export default {
  name: "ListProduct",

  data() {
    return {
      // Utility
      loading: false,
      query_error: false,
      permission_error: false,
      messages: Array(),
      display_button_get_more_product: true,

      products: Array(),
      action: String(),

      OFFSET: 10,

      // limit is number of product add when an user click on button "Afficher plus de produit"
      limit: 10,
      ACTIONS: {
        maybe_not_available: "Produit potentiellement indisponble",
        available: "Produit disponible",
        hide: "Cacher ces produits",
        show: "Afficher ces produits",
      },
    };
  },

  components: {
    Loader,
    Message,
    Modal,
    Drop,
  },

  computed: {
    check_all: {
      get() {
        return false;
      },
      set(value) {
        this.products.forEach((product) => {
          product.check = value;
        });
      },
    },
  },

  methods: {
    get_more_product() {
      this.limit += parseInt(this.OFFSET);
      this.$product.query({ limit: this.limit }).then((response) => {
        this.products = response.body.results;
        if (response.body.next === null) {
          this.display_button_get_more_product = false;
        }
      });
    },

    async apply_action() {
      if (
        this.products.find((product) => product.check === true) === undefined
      ) {
        UIkit.notification(
          "Aucun produit sélctionné. <br>L’action ne peut être appliquée.",
          { status: "warning", pos: "bottom-right" }
        );
      } else {
        let products_check = this.products.filter(
          (product) => product.check === true
        );
        if (this.action === "hide") {
          products_check = products_check.filter((product) => {
            return product.display == true;
          });

          await products_check.forEach((product) => {
            product.display = false;
          });
        } else if (this.action === "show") {
          products_check = products_check.filter((product) => {
            return product.display == false;
          });

          await products_check.forEach((product) => {
            product.display = true;
          });
        } else if (this.action === "maybe_not_available") {
          products_check = products_check.filter((product) => {
            return product.maybe_not_available == false;
          });

          await products_check.forEach((product) => {
            product.maybe_not_available = true;
          });
        } else if (this.action === "available") {
          products_check = products_check.filter((product) => {
            return product.maybe_not_available == true;
          });
          await products_check.forEach((product) => {
            product.maybe_not_available = false;
          });
        }

        await products_check.forEach((product) => {
          this.$product.update({ id: product.id }, product).then(
            (response) => {
              console.log(response);
              if (response.status !== 200) {
                this.query_error = true;
              }
            },
            (response) => {
              if (
                response.status === 403 &&
                response.statusText === "Forbidden"
              ) {
                this.permission_error = true;
              } else {
                this.query_error = true;
              }
            }
          );
        });

        if (this.query_error !== true) {
          this.messages.push({
            id: parseInt(Math.random() * 1000),
            status: "success",
            header: "Produits modifiés",
            body: "Les produits sélectionnés ont bien été modifiés.",
          });
        }

        this.get_products();
      }
    },

    get_products() {
      this.$product.query({ limit: this.limit }).then(
        (response) => {
          response.body.results.forEach((product) => {
            product.check = false;
          });
          this.products = response.body.results;
          if (response.body.next === null) {
            this.display_button_get_more_product = false;
          }
        },
        (response) => {
          if (response.statusText === "Forbidden" && response.status === 403) {
            this.permission_error = true;
          } else {
            this.query_error = true;
          }
        }
      );
    },

    async delete_product(product_id) {
      UIkit.modal("#confirm_delete_" + product_id).hide();
      await this.$product.delete({ id: product_id }).then(
        (response) => {
          this.messages.push({
            id: parseInt(Math.round() * 1000),
            header: "Produit supprimé",
            body: "Le produit a bien été supprimé.",
            status: "success",
          });
        },
        (response) => {
          if (response.status === 400) {
            this.messages.push({
              id: parseInt(Math.round() * 1000),
              header: "Erreur",
              bdoy:
                "Une erreur est survenue, le produit n’a pas pu être supprimé, merci d’actualiser la page, puis réessayer.",
              status: "danger",
            });
          } else if (
            response.status === 403 &&
            response.statusText === "Frobidden"
          ) {
            this.permission_error = true;
          } else {
            this.query_error = true;
          }
        }
      );
      this.get_products();
      UIkit.scroll("", { offset: 150 }).scrollTo("#vue-messages");
    },
  },

  mounted() {
    this.$product = this.$resource(
      "api/citrus/product{/id}",
      { query: "all" },
      {},
      {
        before: () => {
          this.loading = true;
        },

        after: () => {
          this.loading = false;
        },
      }
    );

    this.get_products();
  },
};
</script>
