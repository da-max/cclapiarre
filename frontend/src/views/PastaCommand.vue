<template>
    <div id='pasta-command'>
        <h1 class="uk-text-center">Commander des pâtes</h1>
        <breadcrumb :elements="breadcrumb" />
        <div class="uk-padding uk-margin-auto uk-width-3-5 uk-margin-xlarge-bottom">
            <img src="../assets/Images/Pasta/Pasta3.jpg" alt="Photo de pâtes" class="uk-box-shadow-large" uk-img>
        </div>
        <div class="uk-margin-auto uk-width-3-5@m uk-margin-large-bottom uk-section uk-section-muted uk-padding-large uk-box-shadow-medium" uk-scrollspy="cls:uk-animation-fade; delay: 200">
            <h3 class="uk-title">Comment commander ?</h3>
            <p>
                Pour commander, il suffit de cliquer sur le bouton <span class="uk-text-bold uk-text-primary">"ajouter ce produit à ma commande"</span> qui se trouve en dessous de chaque produit. Puis, il vous faudra 
                choisir le <span class="uk-text-bold uk-text-primary">poids</span> que vous désirez (la disponibilité dépend du porduit choisit) et la quantité que vous souhaitez. Renouvellez cette opération pour autant de produit que vous souhaitez.<br>
                Enfin, n'oubliez pas de renseigner votre <span class="uk-text-bold uk-text-primary">nom, prénom, email et votre numéro de téléphone</span> afin que l'on vous confirme votre commande.
                <span class="uk-text-bold">
                    Tous ces renseignements ne seront en aucun cas diffusés ni utilisés pour vous contactez dans un autre cadre que cette commande, ces informations seront
                    donc supprimées à la fin de la commande.
                </span>
            </p>
        </div>
        <command-pasta />
    </div>
</template>

<script>
import CommandPasta from '../components/pasta/CommandPasta'
import Breadcrumb from '../components/utility/Breadcrumb'

export default {
    name: 'PastaCommand',

    components: {
        CommandPasta,
        Breadcrumb
    },

    data() {
        return {
            breadcrumb: [
                {
                    name: 'Accueil',
                    link: '/'
                },
                {
                    name: 'Pâtes',
                    link: '#',
                    class: 'uk-disabled'
                },
                {
                    name: 'Commander des pâtes'
                }
            ]
        }
    },

    mounted() {
        document.title = 'Commander des pâtes | CC La Piarre'
    },
}
</script>