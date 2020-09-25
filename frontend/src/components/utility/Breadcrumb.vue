<template>
    <section class="uk-margin-large-top uk-margin-xlarge-left uk-text-large uk-text-bold">
        <ul class="uk-breadcrumb">
            <li v-for="element in elements" :key="element.name" :class='element.class'>
                <a v-if='element.link' :href='element.link'>{{ element.name }}</a>
                <span v-else>{{ element.name }}</span>
            </li>
        </ul>
    </section>
</template>

<script>
export default {
  name: 'Breadcrumb',

  props: {
    elements: { type: Array, default: Array }
  }
}
</script>
