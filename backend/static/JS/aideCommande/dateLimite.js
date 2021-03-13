$(document).on("submit", "#formulaireDate", function(e){
    e.preventDefault();
    var jour = $("#id_date_day").val();
    var mois = $('#id_date_month').val();
    var annee = $('#id_date_year').val();
    var messages = $('#messagesJS');

    var message = `Bonjour,

La commande de court-circuit est ouverte, merci de commander vos agrumes avant le ` + jour + "/" + mois + "/" + annee +
`. 
Si vous avez un problème lors de la commande merci de contacter court-circuit en répondant à ce message ou contacter directement l\'administrateur du site à l\'adresse : benhassenm@tutamail.com .
Merci`;

var errorMessage = `<div class="uk-alert-danger" uk-alert>
                        <a class="uk-alert-close" uk-close></a>
                        Vous avez rentré une date qui est après la date limite défini par court-circuit, merci de corriger cette erreur puis de réessayer. 
                        <hr>
                        <span class="uk-text-bold">Si vous rencontrez un problème merci de me contacter par mail : benhassenm@tutamail.com</span>
                    </div>`;
    
    var textarea = $("#message");
    textarea.val(message);
    $.ajax({
        type: "POST",
        url: "/responsable-de-la-commande/insertion-date",
        data:{
            jour:jour,
            mois:mois,
            annee:annee,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(data){
            console.log(data);
            if(data == "erreur"){
                messages.append(errorMessage);                
            }else{
                UIkit.modal("#mail").show();
            }
        }
    });
});
