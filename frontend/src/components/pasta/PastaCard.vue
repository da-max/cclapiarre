<template>
    <div id='pasta-card' class='uk-card-default uk-padding uk-padding-large-top uk-padding-large-bottom' uk-scrollspy='cls:uk-animation-fade; delay: 200'>
        <div class="uk-card-header">
            <slot name='header'>Nom du produit</slot>
        </div>        
        <div class="uk-margin-large-top uk-card-body">
            <slot name='body'></slot>
        </div>
        <div class="uk-card-footer uk-text-center">
            <slot name='footer'></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PastaCard',
}
</script>