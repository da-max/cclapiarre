<template>
    <div id="command-citrus">
        <loader v-show='loading'></loader>
        <modal id='command-recap' :container='true'>
            <template v-slot:header>
                <h3>Récapitulatif de votre commande</h3>
            </template>
            <template v-slot:body>
                <p class="uk-text-center">
                    <span class="uk-label">Vous ếtes connecté.e sous le nom de</span> {{ username }}
                    <span class='uk-label uk-margin-left'>Email</span> {{ email }}
                    <span class="uk-label uk-margin-left">Total de votre commande</span> {{ total_command }} €
                </p>
                <message v-show="send_mail" class='uk-width-3-5@m'>
                    <template v-slot:header>
                        <h3>Mail Récapitulatif</h3>
                    </template>
                    <template v-slot:body>
                        Un mail récapitulatif de votre commande sera envoyé à l'adresse suivante : <span class='uk-text-bold'>{{ email }}</span>.
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
                <button class="uk-button uk-button-primary" type="submit" @click.prevent='commandCitrus()'>Commander</button>
                <button class="uk-button uk-button-default uk-modal-close uk-margin-large-left" type="button">Annuler</button>
            </template>
        </modal>


        <div id="messages" class="uk-width-2-5@m uk-width-3-4 uk-margin-auto uk-margin-xlarge-bottom">
            
            <!-- Display if error = true -->
            <message v-show="query_error" :close='false'>
                <template v-slot:header>
                    Erreur interne
                </template>
                <template v-slot:body>
                        Une erreur est survenue, cela vient de nous, merci d'actualiser la page et de
                        nous contacter si vous rencontrez de nouveau cette erreur.
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
                <span class="uk-label">Vous êtes connecté sous le nom</span> {{ username }} 
                <span class='uk-label'>email</span> {{ email }}
                <br>
                <div class="uk-margin-medium-top">
                    <label class="uk-margin-right uk-form-label" for="checkbox">Recevoir un mail récapitulant ma commande</label><input type="checkbox" id='checkbox' class='uk-checkbox' v-model="send_mail">
                </div>
                <br>
                <p class='uk-text-muted'>Pour changer d'utilisateur cliquez <a href='/compte/changer-utilisateur' class='uk-link'>ici</a></p>
            </div>
            <div class="uk-text-center uk-text-bold uk-text-large uk-margin-medium-bottom"><span class="uk-label">Total actuel de votre commande</span> {{ total_command }} €</div>
            <div class="uk-overflow-auto uk-padding-large uk-padding-remove-left uk-padding-remove-right">
                <table class='uk-table uk-table-divider uk-table-striped uk-table-hover'>
                    <thead>
                        <tr>
                            <th>Nom du produit</th>
                            <th v-show="!has_command">Ma commande</th>
                            <th>Total</th>
                            <th v-for="c in commands" :key="c.id">

                                <drop button_style='default' pos='left'>
                                    <template v-slot:button>{{ c.user.username }}</template>
                                    <template v-slot:header>{{ c.user.username }}</template>
                                    <template v-slot:body>
                                        <button :uk-toggle='"target: #confirm-delete-command-" + c.id' type="button" class="uk-button uk-button-danger">Supprimer</button>
                                    </template>
                                </drop>

                                <modal :close_button='true' :id='"confirm-delete-command-" + c.id'>
                                    <template v-slot:header>
                                        <h3>Supprimer la commande de {{ c.user.username }}</h3>
                                    </template>
                                    <template v-slot:body>
                                        Vous êtes sur le point de supprimer la commande de {{ c.user.username}}, <span class="uk-text-warning uk-text-bold">attention, cette ation est irréversible</span>.
                                    </template>
                                    <template v-slot:footer>
                                        <button class="uk-button uk-button-default uk-margin-medium-right uk-modal-close">Annuler</button>
                                        <button class="uk-button uk-button-danger" @click="delete_command(c.user)">Supprimer</button>
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
                <input type='submit' class="uk-button uk-margin-auto uk-button-primary" @click.prevent="show_recap()" value='Valider ma commande' v-show="!has_command && Object.keys(command).length != 0" id='button-command'>
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
            command: {},
            messages: [],
            email: String(),
            username: String(),
            loading: false,
            send_mail: true,
            query_error: false
        }
    },

    computed: {
        total_command () {

            if (this.has_command == true) {
                return this.commands.filter(c => c.user == this.current_user).total

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

        show_recap () {
            UIkit.modal('#command-recap').show()
        },

        commandCitrus () {
            UIkit.modal('#command-recap').hide()
            this.loading = true


            let formData = new FormData()

            Object.entries(this.command).forEach(c => {
                formData.append(c[0], c[1])
            })

            formData.append('send_mail', this.send_mail)

            this.$resource('commande/create-command').save({}, formData).then(response => {
                
                if (response.data.status == 'success') {
                    this.get_command()
                    this.loading = false
                }
                else {
                    this.messages.push(response.data)
                    UIkit.scroll('#button-command', {offset: 200}).scrollTo('#messages')
                }
                this.loading = false
            },
            response =>{
                this.messages.push({
                        'status': 'danger',
                        'header': 'Erreur',
                        'body': 'Une erreur est survenue, merci de recharger la page est de me contacter si vous rencontrez de nouveau cette erreur.'
                    })
                this.loading = false
            })
        },

        delete_command (id_command) {
            UIkit.modal('#confirm-delete-command-' + id_command).hide()
            this.loading = true

            this.$resource('commande/delete-citrus-command').delete({id_command: id_command}).then((response) => { 
                this.messages.push(response.data)             
                this.get_command()
                this.loading = false
            }, response => {
                this.messages.push({
                        'status': 'danger',
                        'header': 'Erreur',
                        'body': 'Une erreur est survenue, merci de recharger la page est de me contacter si vous rencontrez de nouveau cette erreur.'
                    })
                this.loading = false
            })
        },

        get_command () {
            this.$citrus.query().then(
                (response) => {
                    
                    this.products = response.data.products_list
                    this.users = response.data.users
                    this.total = response.data.total
                    this.has_command = response.data.has_command
                    Object.values(this.products).forEach(product => {
                        this.command[product.name]
                        
                    });
                    this.username = response.data.username
                    this.email = response.data.email
                },
                (response) => {
                    this.messages.push({
                        'status': 'danger',
                        'header': 'Erreur',
                        'body': 'Une erreur est survenue, merci de recharger la page est de me contacter si vous rencontrez de nouveau cette erreur.'
                    })
                    
                }
            )
        }
    },

    mounted() {        
        // Get citrus list
        this.$citrus = this.$resource('api/citrus/product', {}, {}, {
            before: () => {this.loading = true},
            after: () => {this.loading = false}
        })
        this.$citrus.query().then((response) => {
            this.products = response.data
        },
        (response) => {
            this.query_error = true
        })

        // Get command list
        this.$command = this.$resource('api/citrus/command', {}, {}, {
            before: () => {this.loading = true},
            after: () => {this.loading = false}
        })

        this.$command.query().then((response) => {            
            this.commands = response.data            
        }, (response) => {
            this.query_error = true
        })

        // Get amounts
        this.$amount = this.$resource('api/citrus/amount', {}, {}, {
            before: () => {this.loading = true},
            after: () => {this.loading = false}
        })

        this.$amount.query().then((response) => {
            this.amounts = response.data
        }, (response) => {
            this.query_error = true
        })

        // Get current user
        this.$user = this.$resource('api/users/current', {}, {}, {
            before: () => {this.loading = true},
            after: () => {this.loading = false}
        })
        this.$user.query().then((response) => {
            this.current_user = response.data
        },
        (response) => {
            this.query_error = true
        })
    },
}
</script>