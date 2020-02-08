<template>
    <div id="drop" class="uk-inline">
        <button :class="'uk-button uk-button-' +  button_style"><slot name="button"></slot></button>
        <div :uk-drop="'mode:'  + mode + ' ;pos:' + pos">
            <div class="uk-card uk-card-default">
                <div class="uk-card-header">
                    <h4><slot name='header'></slot></h4>
                </div>
                <div class="uk-card-body">
                    <slot name='body'></slot>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Drop',

    props: {
        mode: {type: String, default: 'click'},
        pos: {type: String, default: 'bottom'},
        button_style: {type: String, default: 'default'}
    }
}
</script>