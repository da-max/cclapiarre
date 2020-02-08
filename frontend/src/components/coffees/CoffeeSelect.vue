<template>
    <div id='coffee-select'>
        <div class="uk-margin-medium">
            <label class="uk-form-label" for="id1">Café</label>
            <div class="uk-form-controls">
                <select class="uk-select" v-model='coffee.farm_coop' id="id1">
                    <option selected>Séléctionner un café</option>
                    <option v-for="c in coffees">{{ c.farm_coop }}</option>
                </select>
            </div>
        </div>
        <div v-if="displayWeight" class="uk-margin-medium" >
            <label class="uk-form-label">Poids du café</label>
            <div class="uk-form-controls">
                <select class="uk-select" v-model='coffee.weight'>
                    <option selected>Séléctionner le poids</option>
                    <option>200 grammes</option>
                    <option>1 kg</option>
                </select>
            </div>
        </div>
        <div v-if='displayTypes' class="uk-margin-medium" >
            <label class="uk-form-label">Type de mouture</label>
            <div class="uk-form-controls">
                <select class="uk-select" v-model='coffee.type'>
                    <option selected default>Séléctionner le type de café</option>
                    <option v-for="type in types">{{ type }}</option>
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
        coffees: {type: Object, default: {}},
        coffee: {type: Object, default: {}}

    },

    data() {
        return {
            default_coffee : Object()
        }
    },

    computed: {
        displayWeight () {
            if (this.coffee.farm_coop !== 'Séléctionner un café') {
                return true
            }
            else {
                this.coffee.quantity = 0
                this.coffee.type = 'Séléctionner le type de café'
                this.coffee.weight = 'Séléctionner le poids'
                return false
            }
        },

        displayTypes () {
            if (this.coffee.farm_coop !== 'Séléctionner un café' && this.coffee.weight !== 'Séléctionner le poids') {
                return true
            }
            else {
                this.coffee.quantity = 0
                this.coffee.type = 'Séléctionner le type de café'
                return false
            }
        },

        displayQuantity() {
            if(this.coffee.farm_coop !== 'Séléctionner un café' && this.coffee.weight !== 'Séléctionner le poids' && this.coffee.type !== 'Séléctionner le type de café'){
                return true
            }
            else {
                this.coffee.quantity = 0
                return false
            }
        },

        types () {
            let c = Object.values(this.coffees)
                        
            for (let i = 0; i < c.length; i++) {
                if (c[i].farm_coop == this.coffee.farm_coop) {
                    this.coffee.default_coffee = c[i]
                }
            
            }
            return this.coffee.default_coffee.available_type
        }
    },
}
</script>