<template>
  <div>
    <label
      v-show="displayLabel"
      :for="name"
      :class="['uk-form-label', { 'required-label': required && displayInfo }]"
    >
      {{ label }}
    </label>
    <div class="uk-form-controls">
      <input
        type="number"
        :name="name"
        :step="step"
        :min="min"
        :max="max"
        :placeholder="label"
        :value="value"
        :class="['uk-input', { 'uk-form-danger': value <= 0 }]"
        @input="$emit('input', $event.target.value)"
      >
    </div>
    <div v-show="displayInfo">
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
    <p class="uk-text-muted">
      <slot />
    </p>
  </div>
</template>

<script>
export default {
  name: 'FormInputNumber',
  props: {
    name: {
      type: String,
      required: true
    },
    label: {
      type: String,
      required: true
    },
    value: {
      type: [Number, String],
      required: true
    },
    required: {
      type: Boolean,
      default: true,
      required: false
    },
    min: {
      type: Number,
      default: 0,
      required: false
    },
    max: {
      type: Number,
      default: 100,
      required: false
    },
    step: {
      type: Number,
      default: 1,
      required: false
    },
    displayLabel: {
      type: Boolean,
      default: true,
      required: false
    },
    displayInfo: {
      type: Boolean,
      default: true,
      required: false
    }
  }
}
</script>
