<template>
    <div id='coffee-select'>
        <div class="uk-margin-medium">
            <label class="uk-form-label" for="id1">Café</label>
            <div class="uk-form-controls">
                <select class="uk-select" v-model='coffee.coffee' id="id1">
                    <option v-for="c in coffees" :key="c.id" :value="c">{{ c.farm_coop }}</option>
                </select>
            </div>
        </div>
        <div v-if="displayWeight" class="uk-margin-medium" >
            <label class="uk-form-label">Poids du café</label>
            <div class="uk-form-controls">
                <select class="uk-select" v-model='coffee.weight'>
                    <option>Sélectionner le poids</option>
                    <option value="200">200 grammes</option>
                    <option value="1000">1 kg</option>
                </select>
            </div>
        </div>
        <div v-if='displayTypes' class="uk-margin-medium" >
            <label class="uk-form-label">Type de mouture</label>
            <div class="uk-form-controls">
                <select class="uk-select" v-model='coffee.type'>
                    <option>Sélectionner le type de café</option>
                    <option v-for="type in coffee.coffee.available_type" :key="type.id" :value="type">{{ type.name }}</option>
                </select>
            </div>
        </div>
        <div v-if="displayQuantity" class="uk-margin-medium">
            <label class="uk-form-label">Quantité commandé</label>
            <div class="uk-form-controls">
                <input type="number" class="uk-input" min='0' step="1" placeholder="Quantité commandé" v-model='coffee.quantity'>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Coffee",

    props: {
        index: {type: Number, default: 0},
        coffees: {type: Array, default: []},
        coffee: {type: Object, default: {}}

    },

    data() {
        return {
            default_coffee : Object()
        }
    },

    computed: {
        displayWeight () {
            if (this.coffee.farm_coop !== 'Sélectionner un café') {
                return true
            }
            else {
                this.coffee.quantity = 0
                this.coffee.type = 'Sélectionner le type de café'
                this.coffee.weight = 'Sélectionner le poids'
                return false
            }
        },

        displayTypes () {
            if (this.coffee.farm_coop !== 'Sélectionner un café' && this.coffee.weight !== 'Sélectionner le poids') {
                return true
            }
            else {
                this.coffee.quantity = 0
                this.coffee.type = 'Sélectionner le type de café'
                return false
            }
        },

        displayQuantity() {
            if(this.coffee.farm_coop !== 'Sélectionner un café' && this.coffee.weight !== 'Sélectionner le poids' && this.coffee.type !== 'Sélectionner le type de café'){
                return true
            }
            else {
                this.coffee.quantity = 0
                return false
            }
        }
    },
}
</script>