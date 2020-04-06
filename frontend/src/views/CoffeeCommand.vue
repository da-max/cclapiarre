<template>
    <div id="coffeeCommand">
        <h1 class="uk-text-center">Commander du café</h1>
        <breadcrumb :elements="breadcrumb"></breadcrumb>
        <div class="uk-width-3-5@s uk-margin-auto uk-padding-remove-left uk-padding-remove-right uk-padding"  uk-slider="center: true; autoplay: true; autoplay-interval: 6000; pause-on-hover: false; finite: false">
        
            <div class="uk-position-relative">
            
                <div class="uk-slider-container">
        
                    <ul class="uk-slider-items uk-grid">
                        <li class="uk-width-3-4">
                            <img src="../assets/Images/Coffee/coffee1.jpg" alt="photos de café">
                        </li>
                        <li class="uk-width-3-4">
                                <img src="../assets/Images/Coffee/coffee2.jpg" alt="photos de café">
                        </li>
                        <li class="uk-width-3-4">
                            <img src="../assets/Images/Coffee/coffee.jpg" alt="photos de café">
                        </li>
                        <li class="uk-width-3-4">
                            <img src="../assets/Images/Coffee/coffee1.jpg" alt="photos de café">
                        </li>
                        <li class="uk-width-3-4">
                            <img src="../assets/Images/Coffee/coffee2.jpg" alt="photos de café">
                        </li>
                        <li class="uk-width-3-4">
                            <img src="../assets/Images/Coffee/coffee.jpg" alt="photos de café">
                        </li>
                    </ul>
        
                </div>
        
                <div class="uk-hidden@s uk-light">
                    <a class="uk-position-center-left uk-position-small" href="#" uk-slidenav-previous uk-slider-item="previous"></a>
                    <a class="uk-position-center-right uk-position-small" href="#" uk-slidenav-next uk-slider-item="next"></a>
                </div>
                <div class="uk-visible@s">
                    <a class="uk-position-center-left-out uk-position-small" href="#" uk-slidenav-previous uk-slider-item="previous"></a>
                    <a class="uk-position-center-right-out uk-position-small" href="#" uk-slidenav-next uk-slider-item="next"></a>
                </div>
            </div>
        </div>
        <div class="uk-margin-auto uk-margin-large-bottom uk-width-2-5@m uk-card uk-card-default" uk-scrollspy="cls:uk-animation-fade; delay: 200">
            <div class="uk-text-justify uk-text-bold uk-card-body">
                <span class="uk-text-primary">Choisissez votre café en fonction de la cafetière à laquelle vous le destinez :</span><br>
                <ul class="uk-list uk-list-bullet">
                    <li>Moulu expresso pour une cafetière expresso.</li>
                    <li>Moulu moka pour une cafetière italienne.</li>
                    <li>Moulu piston pour une cafetière à piston.</li>
                    <li>Moulu filtre pour une cafetière filtre.</li>
                </ul>
                <span class="uk-text-primary">
                Vous pouvez aussi acheter votre café en grains et le moudre au fur et à mesure de votre consommation, l'arôme n'en sera que meilleur !
                </span>
                <ul class="uk-list uk-list-bullet">
                    <li>Grain expresso pour cafetière italienne et expresso (la torréfaction est légèrement plus forte).</li>
                    <li>Grain filtre pour une cafetière filtre ou piston (la torréfaction est légèrement plus douce).</li>
                </ul>
            </div>
        </div>
        
        <div class="uk-margin-auto uk-width-3-5@m uk-margin-large-bottom uk-section uk-section-muted uk-padding-large uk-box-shadow-medium" uk-scrollspy="cls:uk-animation-fade; delay: 200">
            <h3 class="uk-title">Comment commander ?</h3>
            <p>
                Bienvenue sur la nouvelle interface de commande de café. Pour commander, il suffit de cliquer sur 
                le bouton <span class="uk-text-bold uk-text-primary">« ajouter ce café à ma commande »</span> qui se trouve en dessous de chaque café. 
                Puis, il vous faudra choisir le <span class="uk-text-bold uk-text-primary">poids</span> que vous désirez (200 grammes ou 1 kg), 
                le <span class="uk-text-bold uk-text-primary">type de mouture</span> en fonction de votre cafetière et la quantité de café que vous souhaitez. 
                Renouvelez cette opération pour autant de café que vous souhaitez.
                
                Enfin, n’oubliez pas de renseigner votre <span class="uk-text-bold uk-text-primary">nom, prénom, e-mail et votre numéro de téléphone</span> afin que l’on vous confirme votre commande. 
                
                <span class="uk-text-bold">
                    Tous ces renseignements ne seront en aucun cas diffusés ni utilisés pour vous contacter dans un autre cadre que cette commande, ces informations seront donc supprimées à la fin de la commande.
                </span>
            </p>
        </div>

        <command-coffees></command-coffees>
    </div>
</template>

<script>
import CommandCoffees from '../components/coffees/CommandCoffees'
import Breadcrumb from '../components/utility/Breadcrumb'

export default {
    name: 'CoffeeCommand',
    components: {
        CommandCoffees,
        Breadcrumb
    },

    data() {
        return {
            breadcrumb: [
                {
                    name: 'Accueil',
                    link: '/',
                },
                {
                    name: 'Café',
                    link: '#',
                    class: 'uk-disabled'
                },
                {
                    name: 'Commander du café'
                }
            ]
        }
    
    },

    mounted() {
        document.title = 'Commander du café | CC La Piarre'
    },
}
</script>