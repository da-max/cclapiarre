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
                            <td>{{ c[0] }}</td>
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



        <form>
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
                            <th v-for="user in users" :key="user[0]">{{ user[0] }}</th>
                        </tr>
                    </thead>
                    <tfoot>
                        <tr>
                            <td>Total</td>
                            <td v-show="!has_command">{{ total_command }} €</td>
                            <td>{{ total }} €</td>
                            <td v-for="user in users" :key="user[0]">{{ user[1] }} €</td> 
                        </tr>
                    </tfoot>
                    <tbody>
                        <tr v-for="product in products" :key="product.name">
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
                            <td v-show="!has_command"><input type="number" min='0' :step='product.step' :max='product.maximum' class='uk-input' :disabled="has_command" v-model="command[product.name]"></td>
                            <td>
                                <span v-if='product.weight != 1'>{{ product.total }} caisse<span v-if="product.total > 1">s</span>
                                    (soit {{ Math.round(product.total * product.weight * 100) / 100 }} kg)
                                </span>
                                <span v-else>{{ product.total }}</span>
                            </td>
                            <td v-for="user in users" :key='user.id'>{{ quantity(user[0], product.amouts) }}</td>
                        </tr> 
                    </tbody>
                </table>
            </div>
            <div class='uk-text-center uk-margin-large'>
                <input type='submit' class="uk-button uk-margin-auto uk-button-primary" @click.prevent="show_recap()" value='Valider ma commande' v-show="!has_command" id='button-command'>
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
            users: {},
            total: Number(),
            has_command: false,
            command: {},
            messages: [],
            email: String(),
            username: String(),
            loading: false,
            send_mail: true
        }
    },

    computed: {
        total_command () {
            if (this.has_command == true){
                return this.users.filter(user => user[0] == this.username)[0][1]
            }
            else {
                let total_command = Number()
                let command_entries = Object.entries(this.command)
                command_entries.forEach(command => {
                
                    total_command += Object.entries(this.products).filter(
                    product => product[1].name == command[0])[0][1].price * command[1]
            
            })
            
            return total_command
            }
        }
    },

    methods: {
        
        quantity (user, amouts_users) {
            for (let i = 0; i < amouts_users.length; i++) {
                if (user === amouts_users[i].user) {
                    return amouts_users[i].quantity
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
                    location.reload()
                }
                else {
                    this.messages.push(response.data)
                    UIkit.scroll('#button-command', {offset: 200}).scrollTo('#messages')
                }
                this.loading = false
            },
            response =>{
                console.log('error');
                this.loading = false
            })
        }
    },

    mounted() {
        this.$citrus = this.$resource('commande/citrus-formate', {}, {}, {
            before: () => {this.loading = true},
            after: () => {this.loading = false}
        }),

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
                console.log('erreur', response);
                
            }
        )
    },
}
</script>