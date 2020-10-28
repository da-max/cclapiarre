<template>
  <div>
    <form action="#">
      <FormInput
        :type="username.type"
        :name="username.name"
        :label="username.label"
        :value="username.value"
        v-model="user.username"
      />

      button.uk-button
    </form>
  </div>
</template>

<script>
import FormInput from '@/components/Utils/Form/FormInput'

export default {
  name: 'LoginForm',
  components: {
    FormInput
  },
  data () {
    return {
      username: {
        type: 'text',
        name: 'username',
        label: 'nom d’utilisateur',
        value: ''
      },
      user: {
        username: ''
      }
    }
  }
}
</script>
