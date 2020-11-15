export default {
  namespaced: true,

  state: () => ({

    alerts: [],
    alertId: 0

  }),

  mutations: {
    ADD_ALERT (state, alert) {
      alert.id = state.alertId
      state.alerts.push(alert)
      state.alertId++
      // eslint-disable-next-line no-undef
      UIkit.scroll(null, { offset: 300 }).scrollTo('#alerts')
    },
    ADD_404 (state) {
      this.commit('alert/ADD_ALERT', {
        id: state.alertId,
        header: true,
        headerContent: 'Ressource introuvable',
        body: 'La ressource demandée n’a pas été trouvée, merci de réessayer.',
        status: 'danger',
        close: true
      })
    },
    ADD_400 (state) {
      this.commit('alert/ADD_ALERT', {
        id: state.alertId,
        header: true,
        headerContent: 'Formulaire incomplet',
        body:
        'Merci de vérifier que vous avez rempli tous les champs du formulaire puis réessayer.',
        status: 'warning',
        close: true
      })
    },
    ADD_500 (state) {
      this.commit('alert/ADD_ALERT', {
        id: state.alertId,
        header: true,
        headerContent: 'Erreur interne',
        body:
        'Une erreur est survenue, merci de réessayer et de me contacter si vous rencontrez de nouveau cette erreur.',
        status: 'danger',
        close: true
      })
    },
    ADD_503 (state) {
      this.commit('alert/ADD_ALERT', {
        id: state.alertId,
        header: true,
        headerContent: 'Service indisponible',
        body:
        'Le service demandé est momentanément indisponible, merci de réessayer ultérieurement.',
        status: 'danger',
        close: true
      })
    },
    ADD_403 (state) {
      this.commit('alert/ADD_ALERT', {
        id: state.alertId,
        header: true,
        headerContent: 'Accès refusé',
        body:
        'L’accès n’est pas autorisé, cela signifie que vous n’avez pas les droits pour accéder à cette page.',
        status: 'danger',
        close: true
      })
    },
    ADD_UNKNOWN (state) {
      this.commit('alert/ADD_ALERT', {
        id: state.alertId,
        header: true,
        headerContent: 'Erreur inconnue',
        body:
        'Une erreur est survenue, merci de réessayer et de me contacter si vous rencontrez de nouveau cette erreur.',
        status: 'danger',
        close: true
      })
    },

    DELETE_ALERT (state, alertId) {
      state.alerts = state.alerts.filter((alert) => alert.id !== alertId)
    }
  }
}
