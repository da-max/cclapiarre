$(document).ready(function(){
	
	var submit = $('#submit');
	var messages = $('#messages');
	var errorMessage = `<div class="uk-alert-danger" uk-alert>
								<a class="uk-alert-close" uk-close></a>
								Vous n'avez rentré aucune quantité, merci de rentrer au moins une quantité pour un produit avant de valider.	
								<hr>
								<span class="uk-text-bold">Si vous rencontrez un problème merci de me contacter par mail : benhassenm@tutamail.com</span>
							</div>`;
	
	submit.click(function(e){
		var commande = $('.uk-input')
		var suite = false;
		for(var i = 0; i < commande.length; i ++){
			if(parseInt(commande[i].value) != 0){
				suite = true
			}
		}
		if(suite == false){
			e.preventDefault()
			messages.append(errorMessage);
		}
	});
});