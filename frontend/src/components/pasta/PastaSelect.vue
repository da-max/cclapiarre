<template>
    <div id='pasta-select'>
        <div class="uk-margin-medium">
            <label for="id1" class="uk-form-label">Produit</label>
            <div class="uk-form-controls">
                <select name="id1" id="id1" class="uk-select" v-model='product.name'>
                    <option selected>Séléctionner un produit</option>
                    <option v-for="p in products" :key="p.id">{{ p.name }}</option>
                </select>
            </div>
            <div class="uk-margin-medium" v-if='displayWeight'>
                <label for="weight" class="uk-form-label">Poids du produit</label>
                <div class="uk-form-controls">
                    <select name="weight" class="uk-select" v-model="product.weight">
                        <option selected>Séléctionner le poids</option>
                        <option v-for="weight in types" :key="weight.weight" :value="weight.weight">{{ weight.weight }} {{ weight.unit }}</option>
                    </select>
                </div>
            </div>
            <div class="uk-margin-medium" v-if="displayAmount">
                <label for="amount" class="uk-form-label">Quantité commandé</label>
                <div class="uk-form-controls">
                    <input type="number" class="uk-input" min="0" step="1" placeholder="Quantité commandé" v-model="product.amount">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Product',

    props: {
        index: {type: Number, default: 0},
        products: {type: Object, default: {}},
        product: {type: Object, default: {}}
    },

    computed: {
        displayWeight () {
            if (this.product.name !== 'Séléctionner un produit') {
                return true
            }
            else {
                this.product.amount = 0
                this.product.weight = 'Séléctionner le poids'
                return false
            }
        },

        displayAmount () {
            if (this.product.name !== 'Séléctionner un produit' && this.product.weight !== 'Séléctionner le poids') {
                return true
            }
            else {
                this.product.amount = 0
                return false
            }
        },

        types () {
            let p = Object.values(this.products)
            
            for (let index = 0; index < p.length; index++) {
                if (p[index].name == this.product.name) {
                    this.product.default_product = p[index]
                }                
            }
            return this.product.default_product.available_product
        }
    },
}
</script>