<template>
  <div id="command-citrus">
    <!-- Loader -->
    <loader v-show="loading"></loader>

    <!-- Sommary command -->
    <modal id="command-recap" :container="true" :center="true">
      <template v-slot:header>
        <h3>Récapitulatif de votre commande</h3>
      </template>
      <template v-slot:body>
        <p class="uk-text-center">
          <span class="uk-label">Vous êtes connecté.e sous le nom de</span>
          {{ currentUser.username }}
          <span class="uk-label uk-margin-left">Email</span>
          {{ currentUser.email }}
          <span class="uk-label uk-margin-left">Total de votre commande</span>
          {{ totalCommand }} €
        </p>
        <message v-show="sendMail" class="uk-width-3-5@m">
          <template v-slot:header>
            <h3>Mail Récapitulatif</h3>
          </template>
          <template v-slot:body>
            Un mail récapitulatif de votre commande sera envoyé à l'adresse
            suivante :
            <span class="uk-text-bold">{{ currentUser.email }}</span
            >. Si vous ne souhaitez pas recevoir ce mail, cliquez
            <button
              class="uk-button uk-button-link uk-text-warning"
              type="button"
              @click="sendMail = false"
            >
              ici
            </button>
          </template>
        </message>
        <table
          class="uk-table uk-table-divider uk-text-center uk-table-striped uk-table-hover"
        >
          <thead>
            <tr>
              <th class="uk-text-center">Produits</th>
              <th class="uk-text-center">Quantité commandée</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in Object.entries(command)" :key="c[0]">
              <td>{{ getProductName(c[0]) }}</td>
              <td>{{ c[1] }}</td>
            </tr>
          </tbody>
        </table>
      </template>
      <template v-slot:footer>
        <button
          class="uk-button uk-button-primary uk-margin-large-right"
          type="submit"
          @click.prevent="addCommandCitrus()"
        >
          Commander
        </button>
        <button
          class="uk-button uk-button-default uk-modal-close"
          type="button"
        >
          Annuler
        </button>
      </template>
    </modal>

    <modal
      id="confirm-update"
      v-if="updateCommand.user !== undefined"
      :close_button="true"
    >
      <template v-slot:header>
        <h3>Modifier la commande ?</h3>
      </template>
      <template v-slot:body>
        <span class="uk-text-warning uk-text-bold">
          Attention, vous êtes sur le point de modifier la commande de
          {{ updateCommand.user.username }}.
        </span>
      </template>
      <template v-slot:footer>
        <button
          class="uk-button uk-button-primary uk-margin-right"
          @click.prevent="updateCommandCitrus(updateCommand.id)"
        >
          Modifier la commande
        </button>
        <button class="uk-button uk-button-default uk-modal-close">
          Annuler
        </button>
      </template>
    </modal>

    <!-- Modal for update command -->
    <modal
      :center="true"
      id="update-command"
      :container="true"
      :close_button="true"
    >
      <template v-slot:header>
        <h3 v-if="updateCommand.user !== undefined">
          Modifier la commande de {{ updateCommand.user.username }}
        </h3>
      </template>
      <template v-slot:body>
        <table
          class="uk-table uk-table-divider uk-table-hover uk-table-striped"
        >
          <thead>
            <tr>
              <td>Nom des produits</td>
              <td v-if="updateCommand.user !== undefined">
                {{ updateCommand.user.username }}
              </td>
              <td>Total</td>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product.id">
              <td>
                <drop button_style="secondary" pos="right">
                  <template v-slot:button>{{ product.name }}</template>
                  <template v-slot:header>{{ product.name }}</template>
                  <template v-slot:body>
                    Prix : {{ product.price }} €
                    <br />
                    <span v-if="product.weight != 1">
                      Poids : {{ product.weight }} kg
                      <br />
                    </span>
                    <div v-html="product.description"></div>
                  </template>
                </drop>
              </td>
              <td>
                <input
                  type="number"
                  min="0"
                  :step="product.step"
                  :max="product.maximum"
                  class="uk-input"
                  v-model="updateCommand[product.id]"
                />
              </td>
              <td>
                <span v-if="product.weight != 1">
                  {{ product.total }} caisse<span v-if="product.total > 1"
                    >s</span
                  >
                  (soit
                  {{ Math.round(product.total * product.weight * 100) / 100 }}
                  kg)
                </span>
                <span v-else>{{ product.total }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </template>
      <template v-slot:footer>
        <a
          v-if="updateCommand.id"
          type="button"
          class="uk-button uk-button-primary uk-margin-right"
          href="#confirm-update"
          uk-toggle
          >Modifier la commande</a
        >
        <button class="uk-button uk-button-default uk-modal-close">
          Annuler
        </button>
      </template>
    </modal>

    <!-- Modal soow before delete all -->
    <modal id="warning-delete-all-command">
      <template v-slot:header>
        <h3 class="text-center">Supprimer toutes les commandes ?</h3>
      </template>
      <template v-slot:body>
        <p>
          Vous êtes sur le point de supprimer toutes les commandes,
          <span class="uk-text-warning uk-text-bold uk-text-uppercase"
            >attention, cette action est irréversible !</span
          >
        </p>
      </template>
      <template v-slot:footer>
        <div class="uk-text-center">
          <a
            type="button"
            class="uk-button uk-button-danger uk-margin-right"
            @click.prevent="deleteAllCommand()"
            >Supprimer toutes les commandes</a
          >
          <button class="uk-button uk-button-default uk-modal-close">
            Annuler
          </button>
        </div>
      </template>
    </modal>

    <section
      class="uk-text-center uk-margin-large-bottom uk-margin-large-top"
      uk-scrollspy="cls:uk-animation-fade; delay:200;"
    >
      <a
        type="button"
        href="/agrumes/recapitulatif-de-la-commande"
        class="uk-button uk-button-secondary uk-padding-small uk-margin-medium-right@m uk-margin-large-right"
        >Générer le récapitulatif PDF de la commande</a
      >
      <a
        @click.prevent="showWarningDeleteAllCommand()"
        v-if="
          currentUser.permissions &&
            currentUser.permissions.find(
              (permission) => permission === 'command.delete_command'
            )
        "
        type="button"
        class="uk-button uk-button-danger uk-padding-small"
        >Supprimer toutes les commandes</a
      >
    </section>

    <div
      id="vue-messages"
      class="uk-width-2-5@m uk-width-3-4 uk-margin-auto uk-margin-xlarge-bottom"
    >
      <!-- Display if error = true -->
      <message v-show="queryError" :close="false" status="danger">
        <template v-slot:header>Erreur interne</template>
        <template v-slot:body>
          Une erreur est survenue, cela vient de nous, merci d'actualiser la
          page et de nous contacter si vous rencontrez de nouveau cette erreur.
        </template>
      </message>

      <!-- Dsiplay if permissionError = true -->
      <message v-show="permissionError" :close="false" status="danger">
        <template v-slot:header>Accès interdit</template>
        <template v-slot:body>
          Il semblerait qui vous n'ayez pas l'autorisation d'accéder à cette
          fonctionnalité du site.
        </template>
      </message>
      <!--- Display if user has alreay command -->
      <message v-show="hasCommand" :close="false">
        <template v-slot:header>Vous avez commandé</template>
        <template v-slot:body>
          Vous avez commandé, si vous souhaitez modifier votre commande merci de
          contacter l'administrateur du site à cette adresse :
          <span class="uk-text-bold">da-max@tutanota.com</span>
        </template>
      </message>
      <message
        v-for="message in messages"
        :key="message.id"
        :status="message.status"
      >
        <template v-slot:header>
          <div v-html="message.header"></div>
        </template>
        <template v-slot:body>
          <div v-html="message.body"></div>
        </template>
      </message>
    </div>

    <form id="form">
      <div class="uk-text-center uk-text-bold uk-margin-medium-bottom">
        <span class="uk-label">Vous êtes connecté sous le nom</span>
        {{ currentUser.username }}
        <span class="uk-label">email</span>
        {{ currentUser.email }}
        <br />
        <div class="uk-margin-medium-top" v-if="!hasCommand">
          <label class="uk-margin-right uk-form-label" for="checkbox"
            >Recevoir un mail récapitulant ma commande</label
          >
          <input
            type="checkbox"
            id="checkbox"
            class="uk-checkbox"
            v-model="sendMail"
          />
        </div>
        <br />
        <p class="uk-text-muted">
          Pour changer d'utilisateur cliquez
          <a href="/compte/changer-utilisateur" class="uk-link">ici</a>
        </p>
      </div>
      <div
        class="uk-text-center uk-text-bold uk-text-large uk-margin-medium-bottom"
      >
        <span class="uk-label">Total actuel de votre commande</span>
        {{ totalCommand }} €
      </div>
      <div
        class="uk-overflow-auto uk-padding-large uk-padding-remove-left uk-padding-remove-right"
      >
        <table
          class="uk-table uk-table-divider uk-table-striped uk-table-hover uk-table-middle"
        >
          <thead>
            <tr>
              <th>Nom du produit</th>
              <th v-if="!hasCommand">Ma commande</th>

              <th>Total</th>
              <th v-for="c in commands" :key="c.id">
                {{ c.user.username }}
                <br />
                <a
                  :title="'Supprimer la commande de ' + c.user.username"
                  type="button"
                  uk-icon="icon: trash; ratio: 2"
                  :uk-toggle="'target: #confirm-delete-command-' + c.id"
                  v-if="
                    currentUser.permissions &&
                      currentUser.permissions.find(
                        (permission) => permission === 'command.delete_command'
                      )
                  "
                ></a>
                <a
                  :title="'Modifier la commande de ' + c.user.username"
                  uk-icon="icon: refresh; ratio: 2"
                  v-if="
                    currentUser.permissions &&
                      currentUser.permissions.find(
                        (permission) => permission === 'command.change_command'
                      )
                  "
                  @click.prevent="getCommandForUpdate(c.id)"
                ></a>

                <modal
                  :close_button="true"
                  :id="'confirm-delete-command-' + c.id"
                  v-if="
                    currentUser.permissions &&
                      currentUser.permissions.find(
                        (permission) => permission === 'command.delete_command'
                      )
                  "
                >
                  <template v-slot:header>
                    <h3>Supprimer la commande de {{ c.user.username }}</h3>
                  </template>
                  <template v-slot:body>
                    Vous êtes sur le point de supprimer la commande de
                    {{ c.user.username }},
                    <span class="uk-text-warning uk-text-bold"
                      >attention, cette ation est irréversible</span
                    >.
                  </template>
                  <template v-slot:footer>
                    <button
                      class="uk-button uk-button-danger uk-margin-medium-right"
                      @click="deleteCommand(c.id)"
                    >
                      Supprimer
                    </button>
                    <button class="uk-button uk-button-default uk-modal-close">
                      Annuler
                    </button>
                  </template>
                </modal>
              </th>
            </tr>
          </thead>
          <tfoot>
            <tr>
              <td>Total</td>
              <td v-show="!hasCommand">{{ totalCommand }} €</td>
              <td>{{ total }} €</td>
              <td v-for="c in commands" :key="c.id">{{ c.total }} €</td>
            </tr>
          </tfoot>
          <tbody>
            <tr v-for="product in products" :key="product.id">
              <td>
                <drop button_style="secondary" pos="right">
                  <template v-slot:button>{{ product.name }}</template>
                  <template v-slot:header>{{ product.name }}</template>
                  <template v-slot:body>
                    Prix : {{ product.price }} €
                    <br />
                    <span v-if="product.weight != 1">
                      Poids : {{ product.weight }} kg
                      <br />
                    </span>
                    <div v-html="product.description"></div>
                  </template>
                </drop>
              </td>
              <td v-show="!hasCommand">
                <input
                  type="number"
                  min="0"
                  :step="product.step"
                  :max="product.maximum"
                  class="uk-input"
                  v-model="command[product.id]"
                />
              </td>
              <td>
                <span v-if="product.weight != 1">
                  {{ product.total }} caisse
                  <span v-if="product.total > 1">s</span>
                  (soit
                  {{ Math.round(product.total * product.weight * 100) / 100 }}
                  kg)
                </span>
                <span v-else>{{ product.total }}</span>
              </td>
              <td v-for="c in commands" :key="c.id">
                {{ quantity(c.user, product) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="uk-text-center uk-margin-large">
        <input
          type="submit"
          class="uk-button uk-margin-auto uk-button-primary"
          @click.prevent="showRecap()"
          value="Valider ma commande"
          v-if="!hasCommand && Object.values(command).length != 0"
          id="button-command"
        />
      </div>
    </form>
  </div>
</template>

<script>
import Drop from "../utility/Drop";
import Message from "../utility/Message";
import Modal from "../utility/Modal";
import Loader from "../utility/Loader";

export default {
  name: "TableCommand",

  components: {
    Drop,
    Message,
    Modal,
    Loader,
  },

  data() {
    return {
      products: {},
      currentUser: {},
      commands: {},
      amounts: [],

      // This object contain command that the user is entering
      command: {},
      updateCommand: {},
      // Messages of display
      messages: [],

      loading: false,
      sendMail: true,

      // Error
      queryError: false,
      permissionError: false,
    };
  },

  computed: {
    totalCommand() {
      if (this.hasCommand === true) {
        const command = this.commands.filter(
          (c) => c.user.id === this.currentUser.id
        );
        return command[0].total;
      }

      let totalCommand = Number();
      let commandEntries = Object.entries(this.command);

      commandEntries.forEach((command) => {
        this.products.forEach((product) => {
          if (product.id === Number(command[0])) {
            totalCommand += product.price * command[1];
          }
        });
      });

      return Math.round(totalCommand * 100) / 100;
    },

    total() {
      let total = 0;
      const command = Object.values(this.commands);
      for (let i = 0; i < command.length; i++) {
        const c = command[i];
        total += c.total;
      }
      return total;
    },

    totalUpdateCommand() {
      let totalCommand = Number();
      let commandEntries = Object.entries(this.updateCommand);

      commandEntries.forEach((command) => {
        this.products.forEach((product) => {
          if (product.id == command[0]) {
            totalCommand += product.price * command[1];
          }
        });
      });

      return totalCommand;
    },

    hasCommand() {
      const command = Object.values(this.commands);

      for (let i = 0; i < command.length; i++) {
        const c = command[i];
        if (c.user.id == this.currentUser.id) {
          return true;
        }
      }
      return false;
    },
  },

  methods: {
    getProductName(idProduct) {
      for (let i = 0; i < this.products.length; i++) {
        const product = this.products[i];
        if (product.id == idProduct) {
          return product.name;
        }
      }
    },

    quantity(user, product) {
      let command = this.commands.find((command) => command.user.id == user.id);
      let amount = command.amounts.find(
        (amount) => amount.product.id == product.id
      );
      if (amount) {
        return amount.amount;
      } else {
        return 0;
      }
      //for (let i = 0; i < this.amounts.length; i++) {
      //  const amount = this.amounts[i];
      //  if (
      //    user.id === amount.command.user.id &&
      //    amount.product.id === product.id
      //  ) {
      //    return amount.amount;
      //  }
      //}
      //return 0;
    },

    showRecap() {
      UIkit.modal("#command-recap").show();
    },

    addCommandCitrus() {
      UIkit.modal("#command-recap").hide();
      let formData = new Object();
      formData["user"] = this.currentUser.id;
      formData["send_mail"] = this.sendMail;
      formData.amounts = {};
      Object.entries(this.command).forEach((c) => {
        formData.amounts[Number(c[0])] = Number(c[1]);
      });

      this.$command.save({}, formData).then(
        (response) => {
          this.messages.push(response.data);

          if (response.data["status"] == "success") {
            this.getCommand();
            this.command = {};
          }
        },
        (response) => {
          if (response.status == 403 && response.statusText == "Forbidden") {
            this.permissionError = true;
          } else {
            this.queryError = true;
          }
        }
      );
    },

    deleteCommand(id_command) {
      UIkit.modal("#confirm-delete-command-" + id_command).hide();
      this.$command.remove({ id: id_command }, {}).then(
        (response) => {
          this.messages.push(response.data);

          if (response.data["status"] == "success") {
            this.getCommand();
            this.command = {};
          }
        },
        (response) => {
          if (response.status == 403 && response.statusText == "Forbidden") {
            this.permissionError = true;
          } else {
            this.queryError = true;
          }
        }
      );
    },

    updateCommandCitrus(idCommand) {
      UIkit.modal("#confirm-update").hide();

      let formData = {};
      formData["user"] = this.updateCommand.user.id;
      formData.amounts = {};

      Object.entries(this.updateCommand).forEach((update) => {
        if (update[0] != "user" && update[0] != "id") {
          formData.amounts[update[0]] = update[1];
        }
      });

      this.$command.update({ id: idCommand }, formData).then(
        (response) => {
          this.messages.push(response.data);
          if (response.data["status"] == "success") {
            this.getCommand();
          }
        },
        (response) => {
          if (response.status == 403 && response.statusText == "Forbidden") {
            this.permissionError = true;
          } else {
            this.queryError = true;
          }
        }
      );
    },

    showWarningDeleteAllCommand() {
      UIkit.modal("#warning-delete-all-command").show();
    },

    deleteAllCommand() {
      UIkit.modal("#warning-delete-all-command").hide();
      this.$command.remove({ id: "destroy_all" }).then(
        (response) => {
          this.messages.push(response.data);
          this.getCommand();
        },
        (response) => {
          this.queryError = true;
        }
      );
    },

    getCommandForUpdate(idCommand) {
      let com = Object();
      let command = this.commands.find((c) => c.id == idCommand);
      command.amounts.forEach((a) => (com[a.product.id] = a.amount));
      com.id = command.id;
      com.user = command.user;
      this.updateCommand = com;
      UIkit.modal("#update-command").show();
    },

    getCommand() {
      // Get citrus list
      this.$citrus.query().then(
        (response) => {
          this.products = response.data;
        },
        (response) => {
          if (response.status == 403 && response.statusText == "Forbidden") {
            this.permissionError = true;
          } else {
            this.queryError = true;
          }
        }
      );

      // Get command list
      this.$command.query().then(
        (response) => {
          this.commands = response.data;
        },
        (response) => {
          if (response.status == 403 && response.statusText == "Forbidden") {
            this.permissionError = true;
          } else {
            this.queryError = true;
          }
        }
      );

      // Get amounts
      //this.$amount.query().then(
      //	response => {
      //		this.amounts = response.data;
      //	},
      //	response => {
      //		if (response.status == 403 && response.statusText == "Forbidden") {
      //			this.permissionError = true;
      //		} else {
      //			this.queryError = true;
      //		}
      //	}
      //);
    },
  },

  mounted() {
    // Define all resourcev (vue-resource)
    this.$citrus = this.$resource(
      "api/citrus/product",
      {},
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

    this.$command = this.$resource(
      "api/citrus/command{/id}",
      {},
      {},
      {
        before: () => {
          this.loading = true;
        },
        after: () => {
          this.loading = false;
          if (this.messages.length !== 0) {
            UIkit.scroll("#footer", { offset: 100 }).scrollTo("#vue-messages");
          }
        },
      }
    );

    //this.$amount = this.$resource(
    //	"api/citrus/amount{/id}",
    //	{},
    //	{},
    //	{
    //		before: () => {
    //			this.loading = true;
    //		},
    //		after: () => {
    //			this.loading = false;
    //		}
    //	}
    //);

    // Get current user
    this.$user = this.$resource(
      "api/users/current",
      {},
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
    this.$user.query().then(
      (response) => {
        this.currentUser = response.data;
        // Get all informations to display on the table
        this.getCommand();
      },
      (response) => {
        if (response.status == 403 && response.statusText == "Forbidden") {
          this.permissionError = true;
        } else {
          this.queryError = true;
        }
      }
    );
  },
};
</script>
