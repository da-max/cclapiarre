<template>
  <form
    uk-grid
  >
    <div
      class="uk-width-1-2@m"
    >
      <FormInput
        name="username"
        label="Nom d’utilisateur"
        :value="member.username"
        @input="updateUsername"
      />
      <FormInput
        name="email"
        label="Mail"
        type="mail"
        :value="member.email"
        @input="updateEmail"
      />
      <FormInput
        v-if="!member.id"
        name="password"
        type="password"
        label="Mot de passe"
        :value="member.password"
        :error="member.password !== member.passwordConfirm"
        @input="updatePassword"
      />
      <FormInput
        v-if="!member.id"
        name="password"
        type="password"
        label="Confirmer le mot de passe"
        :value="member.passwordConfirm"
        :error="member.password !== member.passwordConfirm"
        @input="updatePasswordConfirm"
      />
      <div v-if="!loading">
        <span class="uk-form-label">Groupes</span>
        <div class="uk-overflow-auto uk-height-medium">
          <div
            v-for="group in groups"
            :key="group.id"
            class="uk-form-controls"
          >
            <label :for="group.name">
              <input
                :id="group.name"
                type="checkbox"
                :name="group.name"
                :value="group.id"
                class="uk-checkbox"
                :checked="member.groups.find(g => g.id === group.id)"
                @change="updateGroup"
              >
              {{ group.name }}</label>
          </div>
        </div>
      </div>
      <div v-else>
        Chargement en cours…
      </div>
    </div>
    <div
      class="uk-width-1-2@m"
    >
      <FormInput
        name="lastName"
        label="Nom de famille"
        :value="member.lastName"
        @input="updateLastName"
      />
      <FormInput
        name="firstName"
        label="Prénom"
        :value="member.firstName"
        @input="updateFirstName"
      />
      <FormInput
        name="phoneNumber"
        label="Numéro de téléphone"
        :value="member.phoneNumber"
        @input="updatePhoneNumber"
      />
      <div v-if="!loading">
        <span class="uk-form-label">Permissions</span>
        <div class="uk-overflow-auto uk-height-medium">
          <div
            v-for="permission in permissions"
            :key="permission.id"
            class="uk-form-controls"
          >
            <label :for="permission.name">
              <input
                :id="permission.name"
                type="checkbox"
                :name="permission.name"
                :value="permission.id"
                class="uk-checkbox"
                :checked="member.userPermissions.find(p => p.id === permission.id)"
                @change="updatePermission"
              >
              {{ permission.contentType.appLabel }}/{{ permission.name }}</label>
          </div>
        </div>
      </div>
      <div v-else>
        Chargement en cours…
      </div>
    </div>
  </form>
</template>

<script>
import useMember from '@/composition/registration/useMember'

import FormInput from '@/components/Utils/Form/FormInput'

export default {
    name: 'MemberForm',
    components: {
        FormInput
    },
    setup () {
        const {
            member,
            getPermissions,
            getGroups,
            groups,
            password,
            passwordConfirm,
            permissions,
            updateEmail,
            updateFirstName,
            updateGroup,
            updateLastName,
            updatePassword,
            updatePasswordConfirm,
            updatePermission,
            updatePhoneNumber,
            updateUsername
        } = useMember()

        const { loading: PermissionLoading } = getPermissions()
        const { loading: GroupLoading } = getGroups()

        return {
            member,
            loading: PermissionLoading || GroupLoading,
            password,
            passwordConfirm,
            permissions,
            groups,
            updateEmail,
            updateFirstName,
            updateGroup,
            updateLastName,
            updatePassword,
            updatePasswordConfirm,
            updatePermission,
            updatePhoneNumber,
            updateUsername
        }
    }
}
</script>
