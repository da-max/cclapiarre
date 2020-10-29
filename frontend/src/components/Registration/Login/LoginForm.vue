<template>
  <div>
    <form action="#">
      <p class="uk-text-danger uk-text-bold" v-if="error">Utilisateur inconnu ou mot de passe incorrect.</p>
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

      <UtilsButton @click="loginUser"> Se connecter </UtilsButton>
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
      error: false,
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
      const response = await this.$store.dispatch('auth/loginUser', this.user)

      if (response.error) {
        this.error = true
      } else {
        this.$store.commit('alert/ADD_ALERT', {
          header: true,
          headerContent: `Bienvenue ${this.$store.state.auth.currentUser.username}`,
          body: `Vous êtes maintenant connecté sous le nom ${this.$store.state.auth.currentUser.username}.`,
          status: 'success',
          close: true
        })
        if (this.$route.query.next) {
          this.$router.push(this.$route.query.next)
        }
      }
    }
  }
}
</script>
