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
      <FormInput
        :type="password.type"
        :name="password.name"
        :label="password.label"
        :value="password.value"
        v-model="user.password"
      />

      <UtilsButton @click="loginUser">
        Se connecter
      </UtilsButton>
    </form>
  </div>
</template>

<script>
import FormInput from '@/components/Utils/Form/FormInput'
import UtilsButton from '@/components/Utils/UtilsButton'

export default {
  name: 'LoginForm',
  components: {
    FormInput,
    UtilsButton
  },
  data () {
    return {
      password: {
        type: 'password',
        name: 'password',
        label: 'Mot de passe',
        value: ''
      },
      username: {
        type: 'text',
        name: 'username',
        label: 'Nom d’utilisateur',
        value: ''
      },
      user: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async loginUser () {
      const user = await this.$store.dispatch('loginUser', this.user)
      console.log(user)
      if (user.error) {
        alert(user.error)
      } else {
        alert('Thank you for you signing in ' + user.username)
      }
    }
  }
}
</script>
