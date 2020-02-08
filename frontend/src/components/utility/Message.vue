<template>
    <div id="message" class='uk-margin-auto uk-margin-medium uk-box-shadow-hover-medium uk-border-rounded'>
        <div :class="'uk-alert-' + status" uk-alert>
            <a v-show="close" class="uk-alert-close" uk-close></a>
            <div class="uk-text-bold uk-text-center uk-margin-small-bottom">
                <slot name="header">
                    <h5>Message</h5>
                </slot>
            </div>
            <slot name="body"></slot>
            <hr>
            <slot name="footer">
                Si vous rencontrez un problème, merci de me contacter à l'adresse 
                mail <span class="uk-text-bold">da-max@tutanota.com</span>
            </slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Message',

    props: {
        status: {type: String, default: 'primary'},
        close: {type: Boolean, default: true}
    }
}
</script>