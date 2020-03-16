<template>
    <div id="command-citrus">
        <!-- Loader -->
        <loader v-show='loading'></loader>

        <!-- Sommary command -->
        <modal id='command-recap' :container='true' :center='true'>
            <template v-slot:header>
                <h3>Récapitulatif de votre commande</h3>
            </template>
            <template v-slot:body>
                <p class="uk-text-center">
                    <span class="uk-label">Vous ếtes connecté.e sous le nom de</span> {{ current_user.username }}
                    <span class='uk-label uk-margin-left'>Email</span> {{ current_user.email }}
                    <span class="uk-label uk-margin-left">Total de votre commande</span> {{ total_command }} €
                </p>
                <message v-show="send_mail" class='uk-width-3-5@m'>
                    <template v-slot:header>
                        <h3>Mail Récapitulatif</h3>
                    </template>
                    <template v-slot:body>
                        Un mail récapitulatif de votre commande sera envoyé à l'adresse suivante : <span class='uk-text-bold'>{{ current_user.email }}</span>.
                        Si vous ne souahitez pas recevoir ce mail, cliquez <button class="uk-button uk-button-link uk-text-warning" type="button" @click="send_mail = false">ici</button>
                    </template>
                </message>
                <table class="uk-table uk-table-divider uk-text-center uk-table-striped uk-table-hover">
                    <thead>
                        <tr>
                            <th class='uk-text-center'>Produits</th>
                            <th  class='uk-text-center'>Quantité commandée</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="c in Object.entries(command)" :key="c[0]">
                            <td>{{ get_product_name(c[0]) }}</td>
                            <td>{{ c[1] }}</td>
                        </tr>
                    </tbody>
                </table>
            </template>
            <template v-slot:footer>
                <button class="uk-button uk-button-primary uk-margin-large-right" type="submit" @click.prevent='add_command_citrus()'>Commander</button>
                <button class="uk-button uk-button-default uk-modal-close" type="button">Annuler</button>
            </template>
        </modal>
        
        <modal id="confirm-update" v-if="update_command.user != undefined" :close_button='true'>
            <template v-slot:header>
                <h3>Modifier la commande ?</h3>
            </template>
            <template v-slot:body>
                <span class="uk-text-warning uk-text-bold">Attention, vous êtes sur le point de modifier la commande de {{ update_command.user.username }}.</span>.
            </template>
            <template v-slot:footer>
                <button class="uk-button uk-button-primary uk-margin-right" @click.prevent="update_command_citrus(update_command.id)">Modifier la commande</button>
                <button class="uk-button uk-button-default uk-modal-close">Annuler</button>
            </template>
        </modal>

        <!-- Modal for update command -->
        <modal :center='true' id="update-command" :container='true' :close_button='true'>
            <template v-slot:header>
                <h3 v-if="update_command.user != undefined">Modifier la commande de {{ update_command.user.username }}</h3>
            </template>
            <template v-slot:body>
                <table class="uk-table uk-table-divider uk-table-hover uk-table-striped">
                    <thead>
                        <tr>
                            <td>Nom des produits</td>
                            <td v-if="update_command.user != undefined" >{{ update_command.user.username }}</td>
                            <td>Total</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="product in products" :key="product.id">
                            <td>
                                <drop button_style='secondary' pos='right'>
                                    <template v-slot:button>{{ product.name }}</template>
                                    <template v-slot:header>{{ product.name }}</template>
                                    <template v-slot:body>
                                        Prix : {{ product.price }} €<br>
                                        <span v-if="product.weight != 1">Poids : {{ product.weight }} kg<br></span>
                                        <div v-html="product.description"></div>
                                    </template>
                                </drop>
                            </td>
                            <td><input type="number" min='0' :step='product.step' :max='product.maximum' class='uk-input' v-model="update_command[product.id]"></td>
                            <td>
                                <span v-if='product.weight != 1'>{{ product.total }} caisse<span v-if="product.total > 1">s</span>
                                    (soit {{ Math.round(product.total * product.weight * 100) / 100 }} kg)
                                </span>
                                <span v-else>{{ product.total }}</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </template>
            <template v-slot:footer>
                <a v-if="update_command.id" type="button" class="uk-button uk-button-primary uk-margin-right" href='#confirm-update' uk-toggle>Modifier la commande</a>
                <button class="uk-button uk-button-default uk-modal-close">Annuler</button>
            </template>
        </modal>

        <!-- Modal soow before delete all -->
        <modal id="warning-delete-all-command">
            <template v-slot:header>
                <h3 class="text-center">Supprimer toutes les commandes ?</h3>
            </template>
            <template v-slot:body>
                <p>Vous êts sur le point de supprimer toutes les commandes, <span class="uk-text-warning uk-text-bold uk-text-uppercase">attention, cette action est irréversible !</span></p>
            </template>
            <template v-slot:footer>
                <div class="uk-text-center">
                    <a type="button" class="uk-button uk-button-danger uk-margin-right" @click.prevent="delete_all_command()">Supprimer toutes les commandes</a>
                    <button class="uk-button uk-button-default uk-modal-close">Annuler</button>
                </div>
            </template>
        </modal>
        
        <section class="uk-text-center uk-margin-large-bottom uk-margin-large-top" uk-scrollspy="cls:uk-animation-fade; delay:200;">
            <a type="button" href="/commande/recapitulatif-de-la-commande" class="uk-button uk-button-secondary uk-padding-small uk-margin-medium-right@m uk-margin-large-right">Générer le récapitulatif PDF de la commande</a>
            <a @click.prevent="show_warning_delete_all_command()" v-if="current_user.permissions.find(permission => permission === 'command.delete_command')" type="button" class="uk-button uk-button-danger uk-padding-small">Supprimer toutes les commandes</a>
        </section>

        <div id="messages" class="uk-width-2-5@m uk-width-3-4 uk-margin-auto uk-margin-xlarge-bottom">
        
            <!-- Display if error = true -->
            <message v-show="query_error" :close='false' status='danger'>
                <template v-slot:header>
                    Erreur interne
                </template>
                <template v-slot:body>
                        Une erreur est survenue, cela vient de nous, merci d'actualiser la page et de
                        nous contacter si vous rencontrez de nouveau cette erreur.
                </template>
            </message>

            <!-- Dsiplay if permission_error = true -->
            <message v-show="permission_error" :close='false' status='danger'>
                <template v-slot:header>
                    Accès interdit
                </template>
                <template v-slot:body>
                    Il semblerait qui vous n'ayez pas l'autorisation d'accéder à cette fonctionnalité du site.
                </template>
            </message>
            <!--- Display if user has alreay command -->
            <message v-show="has_command" :close='false'>
                <template v-slot:header>
                    Vous avez déjà commandé
                </template>
                <template v-slot:body>
                    Vous avez déjà commandé, si vous souhaitez modifier votre commande merci 
                    de contacter l'administrateur du site à cette adresse : <span class='uk-text-bold'>da-max@tutanota.com</span>
                </template>
            </message>
            <message v-for="message in messages" :key="message.id" :status='message.status'>
                <template v-slot:header>
                    <div v-html="message.header"></div>
                </template>
                <template v-slot:body>
                    <div v-html="message.body"></div>
                </template>
            </message>
        </div>

        <form id="form">
            <div class='uk-text-center uk-text-bold uk-margin-medium-bottom'>
                <span class="uk-label">Vous êtes connecté sous le nom</span> {{ current_user.username }} 
                <span class='uk-label'>email</span> {{ current_user.email }}
                <br>
                <div class="uk-margin-medium-top">
                    <label class="uk-margin-right uk-form-label" for="checkbox">Recevoir un mail récapitulant ma commande</label><input type="checkbox" id='checkbox' class='uk-checkbox' v-model="send_mail">
                </div>
                <br>
                <p class='uk-text-muted'>Pour changer d'utilisateur cliquez <a href='/compte/changer-utilisateur' class='uk-link'>ici</a></p>
            </div>
            <div class="uk-text-center uk-text-bold uk-text-large uk-margin-medium-bottom"><span class="uk-label">Total actuel de votre commande</span> {{ total_command }} €</div>
            <div class="uk-overflow-auto uk-padding-large uk-padding-remove-left uk-padding-remove-right">
                <table class='uk-table uk-table-divider uk-table-striped uk-table-hover uk-table-middle'>
                    <thead>
                        <tr>
                            <th>Nom du produit</th>
                            <th v-if="!has_command">Ma commande</th>

                            <th>Total</th>
                            <th v-for="c in commands" :key="c.id">
                                {{ c.user.username }}<br>
                                <a :title="'Supprimer la commande de ' + c.user.username" type="button" uk-icon='icon: trash; ratio: 2' :uk-toggle='"target: #confirm-delete-command-" + c.id' v-if="current_user.permissions.find(permission => permission === 'command.delete_command')"></a>
                                <a :title="'Modifier la commande de ' + c.user.username" uk-icon='icon: refresh; ratio: 2' v-if="current_user.permissions.find(permission => permission === 'command.change_command')" @click.prevent="get_command_for_update(c.id)"></a>

                                <modal :close_button='true' :id='"confirm-delete-command-" + c.id' v-if="current_user.permissions.find(permission => permission === 'command.delete_command')">
                                    <template v-slot:header>
                                        <h3>Supprimer la commande de {{ c.user.username }}</h3>
                                    </template>
                                    <template v-slot:body>
                                        Vous êtes sur le point de supprimer la commande de {{ c.user.username}}, <span class="uk-text-warning uk-text-bold">attention, cette ation est irréversible</span>.
                                    </template>
                                    <template v-slot:footer>
                                        <button class="uk-button uk-button-danger uk-margin-medium-right" @click="delete_command(c.id)">Supprimer</button>
                                        <button class="uk-button uk-button-default uk-modal-close">Annuler</button>
                                    </template>
                                </modal>
                            </th>
                        </tr>
                    </thead>
                    <tfoot>
                        <tr>
                            <td>Total</td>
                            <td v-show="!has_command">{{ total_command }} €</td>
                            <td>{{ total }} €</td>
                            <td v-for="c in commands" :key="c.id">{{ c.total }} €</td> 
                        </tr>
                    </tfoot>
                    <tbody>
                        <tr v-for="product in products" :key="product.id">
                            <td>
                                <drop button_style='secondary' pos='right'>
                                    <template v-slot:button>{{ product.name }}</template>
                                    <template v-slot:header>{{ product.name }}</template>
                                    <template v-slot:body>
                                        Prix : {{ product.price }} €<br>
                                        <span v-if="product.weight != 1">Poids : {{ product.weight }} kg<br></span>
                                        <div v-html="product.description"></div>
                                    </template>
                                </drop>
                            </td>
                            <td v-show="!has_command"><input type="number" min='0' :step='product.step' :max='product.maximum' class='uk-input' v-model="command[product.id]"></td>
                            <td>
                                <span v-if='product.weight != 1'>{{ product.total }} caisse<span v-if="product.total > 1">s</span>
                                    (soit {{ Math.round(product.total * product.weight * 100) / 100 }} kg)
                                </span>
                                <span v-else>{{ product.total }}</span>
                            </td>
                            <td v-for="c in commands" :key='c.id'>{{ quantity(c.user, product) }}</td>
                        </tr> 
                    </tbody>
                </table>
            </div>
            <div class='uk-text-center uk-margin-large'>
                <input type='submit' class="uk-button uk-margin-auto uk-button-primary" @click.prevent="show_recap()" value="Valider ma commande" v-if="!has_command && Object.values(command).length != 0" id='button-command'>
            </div>
        </form>
    </div>
</template>

<script>
import Drop from '../utility/Drop'
import Message from '../utility/Message'
import Modal from '../utility/Modal'
import Loader from '../utility/Loader'

export default {
    name: 'TableCommand',

    components: {
        Drop,
        Message,
        Modal,
        Loader
    },

    data() {
        return {
            products: {},
            current_user: {},
            commands: {},
            amounts: [],

            // This object contain command that the user is entering
            command: {},
            update_command: {},
            // Messages of display
            messages: [],

            loading: false,
            send_mail: true,

            // Error 
            query_error: false,
            permission_error: false,
        }
    },

    computed: {
        total_command () {

            if (this.has_command == true) {
                const command = this.commands.filter(c => c.user.id == this.current_user.id)
                return command[0].total
            }

            let total_command = Number()
            let command_entries = Object.entries(this.command)
            
            command_entries.forEach(command => {
                this.products.forEach(product => {
                    if (product.id == command[0]) {
                        total_command += product.price * command[1]
                    }
                })
            
            })
            
            return total_command
        },

        total() {
            let total = 0
            const command = Object.values(this.commands)
            for (let i = 0; i < command.length; i++) {
                const c = command[i];
                total += c.total
            }
            return total
        },

        total_update_command () {
            let total_command = Number()
            let command_entries = Object.entries(this.update_command)
            
            command_entries.forEach(command => {
                this.products.forEach(product => {
                    if (product.id == command[0]) {
                        total_command += product.price * command[1]
                    }
                })
            })
            
            return total_command
        },

        has_command () {
            const command = Object.values(this.commands)
            
            for (let i = 0; i < command.length; i++) {
                const c = command[i];
                if (c.user.id == this.current_user.id) {
                    return true
                }
            }
            return false
        },
    },

    methods: { 

        get_product_name (id_product) {

            for (let i = 0; i < this.products.length; i++) {
                const product = this.products[i];
                if (product.id == id_product) {
                    return product.name
                }   
            }

        },

        quantity (user, product) {
            for (let i = 0; i < this.amounts.length; i++) {
                const amount = this.amounts[i];
                if (user.id === amount.command.user.id && amount.product.id === product.id) {
                    return amount.amount
                }
            }
            return 0
        },

        show_recap () {UIkit.modal('#command-recap').show()},

        add_command_citrus () {
            UIkit.modal('#command-recap').hide()
            let formData = new FormData()
            formData.append('user', parseInt(this.current_user.id))
            console.log(Number(this.send_mail));
            formData.append('send_mail',  Number(this.send_mail))
            Object.entries(this.command).forEach(c => {
                formData.append(c[0], c[1])
            })
            this.$command.save({}, formData).then((response) => {
                
                this.messages.push(response.data)
                
                if (response.data['status'] == 'success') {
                    this.get_command()
                    this.command = {}
                }
            }, (response) => {
                    if (response.status == 403 && response.statusText == "Forbidden") { this.permission_error = true }
                    else { this.query_error = true }
            })
        },

        delete_command (id_command) {
            UIkit.modal('#confirm-delete-command-' + id_command).hide()        
            this.$command.remove({id: id_command}, {}).then((response) => { 
                
                this.messages.push(response.data)
            
                if (response.data['status'] == 'success') { 
                    this.get_command()
                    this.command = {}
                }
            
            }, (response) => { 

                if (response.status == 403 && response.statusText == 'Forbidden') { this.permission_error = true }
                else { this.query_error = true }
            
            })
        },

        update_command_citrus (id_command) {
            UIkit.modal('#confirm-update').hide()
            
            let form_data = new FormData()
            form_data.append('user_id', this.update_command.user.id)
            
            Object.entries(this.update_command).forEach(update_c => {
                if (update_c[0] != 'user' && update_c[0] != 'id') { form_data.append(update_c[0], update_c[1]) }
            })
            
            this.$command.update({id: id_command}, form_data).then(response => {
                this.messages.push(response.data)
                if (response.data['status'] == 'success') {
                    this.get_command()
                }
            }, response => {
                if (response.status == 403 && response.statusText == 'Forbidden') { this.permission_error = true }
                else { this.query_error = true }
            })
        },

        show_warning_delete_all_command() { UIkit.modal('#warning-delete-all-command').show() },

        delete_all_command() {
            UIkit.modal('#warning-delete-all-command').hide()
            this.$command.remove({id: 'destroy_all'}).then((response) => {
                this.messages.push(response.data)
                this.get_command()
            }, (response) => {
                this.query_error = true
            })
        }, 
        get_command_for_update(id_command) {
            let com = {}
            let command = this.commands.find(c => c.id == id_command)
            com.user = command.user
            com.id = command.id
            for (let i = 0; i < command.product.length; i++) {
                const product = command.product[i];
                com[product.id] = this.quantity(command.user, product)
            }
            this.update_command = com
            UIkit.modal('#update-command').show()
          
        },

        get_command () {
            // Get citrus list
            this.$citrus.query().then((response) => {
                this.products = response.data
            },
            (response) => {
                if (response.status == 403 && response.statusText == 'Forbidden') { this.permission_error = true }
                else { this.query_error = true }
            })

            // Get command list
            this.$command.query().then((response) => {            
                this.commands = response.data            
            }, (response) => {
                if (response.status == 403 && response.statusText == 'Forbidden') { this.permission_error = true }
                else { this.query_error = true }
            })

            // Get amounts
            this.$amount.query().then((response) => {
                this.amounts = response.data
            }, (response) => {
                if (response.status == 403 && response.statusText == 'Forbidden') { this.permission_error = true }
                else { this.query_error = true }
            })
        }
    },

    mounted() {
        
        // Define all resourcev (vue-resource)
        this.$citrus = this.$resource('api/citrus/product', {}, {}, {
            before: () => {this.loading = true},
            after: () => {this.loading = false}
        })

        this.$command = this.$resource('api/citrus/command{/id}', {}, {}, {
            before: () => {this.loading = true},
            after: () => {this.loading = false
                if (this.messages.length !== 0) { UIkit.scroll('#footer', {offset: 100}).scrollTo('#messages') }
            }
        })

        this.$amount = this.$resource('api/citrus/amount{/id}', {}, {}, {
            before: () => {this.loading = true},
            after: () => {this.loading = false}
        })

        // Get all informations to display on the table
        this.get_command()

        // Get current user
        this.$user = this.$resource('api/users/current', {}, {}, {
            before: () => {this.loading = true},
            after: () => {this.loading = false}
        })
        this.$user.query().then((response) => {
            this.current_user = response.data

        },
        (response) => {
            if (response.status == 403 && response.statusText == 'Forbidden') { this.permission_error = true }
            else { this.query_error = true }
        })
        
    },
}
</script>