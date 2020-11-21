<template>
  <div>
    <label
      v-show="displayLabel"
      :for="name"
      :class="['uk-form-label', { 'required-label': required }]"
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
        @input="$emit('input', $event.target.value)"
        :class="['uk-input', { 'uk-form-danger': value <= 0 }]"
      />
    </div>
    <p v-if="required" class="uk-text-muted">Ce champ est requis.</p>
    <p v-else class="uk-text-muted">Ce champ est optionnel.</p>
    <p class="uk-text-muted"><slot></slot></p>
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
      type: Number,
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
    }
  }
}
</script>
