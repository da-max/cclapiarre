<template>
	<div id='list-product'>
    	<loader v-show='loading'></loader>

    	<div id="vue-messages" class="uk-width-2-5@m uk-width-3-4 uk-margin-auto uk-margin-xlarge-bottom">
			<message v-show="query_error" :close="false" status="danger">
				<template v-slot:header>Erreur interne</template>
				<template v-slot:body>
                    Une erreur est survenue, cela vient de nous, merci d'actualiser la
                    page et de nous contacter si vous rencontrez de nouveau cette erreur.
                </template>
			</message>

			<message v-show="permission_error" :close="false" status="danger">
				<template v-slot:header>Accès interdit</template>
				<template v-slot:body>
					Il semblerait qui vous n'ayez pas l'autorisation d'accéder à cette
					fonctionnalité du site.
				</template>
			</message>

			<message v-for="message in messages" :key="message.id" :status="message.status">
				<template v-slot:header>
					<div v-html="message.header"></div>
				</template>
				<template v-slot:body>
					<div v-html="message.body"></div>
				</template>
			</message>
		</div>

		<div class="uk-width-3-5@m uk-margin-auto">
			<table class="uk-table uk-table-divider uk-striped uk-table-hover">
				<thead>
					<tr>
						<th>Nom du produit</th>
						<th>Poids du produit</th>
						<th>Prix du produit</th>
						<th>Produit afficher</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="product in products" :key='product.id'>
						<td>{{ product.name }}</td>
						<td>{{ product.weight }} kg</td>
						<td>{{ product.price }} €</td>
						<td>{{ product.display	 }}</td>
					</tr>
				</tbody>
			</table>
		</div>
        <div v-for="product in products" :key='product.id'>
            {{ product }}
        </div>
    </div>
</template>

<script>
import Loader from "../utility/Loader";
import Message from "../utility/Message";

export default {
	name: "ListProduct",

	data() {
		return {
			// Utility
			loading: false,
			query_error: false,
			permission_error: false,
			messages: Object(),

			products: Array()
		};
	},

	components: {
        Loader,
        Message
	},

	mounted() {
		this.$product = this.$resource(
			"api/citrus/product{/id}",
			{},
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

		this.$product.query({ query: "all" }).then(
			response => {
				this.products = response.body;
			},
			response => {
				if (this.status === "Forbidden" && this.status_code === 403) {
					this.permission_error = true;
				} else {
					this.query_error = true;
				}
			}
		);
	}
};
</script>