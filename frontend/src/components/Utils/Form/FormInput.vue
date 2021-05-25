<template>
  <div>
    <label
      :for="name"
      :class="['uk-form-label', { 'required-label': required }]"
    >{{ label }}</label>
    <div class="uk-form-controls">
      <input
        :required="required"
        :type="type"
        :name="name"
        :class="['uk-input', {'uk-form-danger': error}]"
        step="0.01"
        :placeholder="label"
        :value="value"
        @input="$emit('input', $event.target.value)"
      >
    </div>
    <p
      v-if="required"
      class="uk-text-muted"
    >
      Ce champ est requis.
    </p>
    <p
      v-else
      class="uk-text-muted"
    >
      Ce champ est optionnel.
    </p>
  </div>
</template>

<script>
export default {
    name: 'FormInput',
    props: {
        name: {
            type: String,
            default: 'text',
            required: true
        },
        type: {
            type: String,
            default: 'text'
        },
        label: {
            type: String,
            required: true
        },
        value: {
            type: [String, Number],
            required: true
        },
        required: {
            type: Boolean,
            default: true,
            required: false
        },
        error: {
            type: Boolean,
            default: false,
            required: false
        }
    }
}
</script>
