
$(function()
{
    var send = false;
    $(document).on("submit", "#form", function(e){
        if (send == false)
        {
            e.preventDefault();
            $("#loader").removeAttr("hidden")
            var form = $(this);
            var modal = $("#note");
            var html = "";
            var message = $('#messagesJS');
            var formSubmit = $('#formSubmit');

            $.ajax({
                type: "POST",
                url: "/cafe/calcul-de-la-commande",
                data: form.serialize(),
                success:function(data){
                    $("#loader").attr("hidden", 'hidden');
                    if (data['retour'] == false)
                    {
                        message.html(`<div class="uk-alert-danger" uk-alert>
                            <a class="uk-alert-close" uk-close></a>
                            <p>Une erreur est survenue, merci d'actualisez la page puis réessayez. <span class="uk-text-bold">Un mail a été envoyé automatiquement à l'administrateur du site, il vous recontactera rapidement.</span></p> 
                            <hr>
                            <span class="uk-text-bold">Si vous rencontrez un problème merci de me contacter par mail : benhassenm@tutamail.com</span>
                        </div>`);
                        UIkit.scroll(formSubmit).scrollTo("#top");
                    }
                    else if (data['retour'] == "Info") {
                        message.html(`<div class="uk-alert-danger" uk-alert>
                        <a class="uk-alert-close" uk-close></a>
                        <p>Une erreur est survenue, merci de vérifier que vous avez remplis les champs obligatoires puis réessayez.</p> 
                        <hr>
                        <span class="uk-text-bold">Si vous rencontrez un problème merci de me contacter par mail : benhassenm@tutamail.com</span>
                    </div>`);
                       UIkit.scroll(formSubmit).scrollTo("#top");

		    }
		    else if (data['retour'] == "Nb"){
                        message.html(`<div class="uk-alert-danger" uk-alert>
                        <a class="uk-alert-close" uk-close></a>
                        <p>Une erreur est survenue, merci de vérifier que vous n'avez pas mis de <span class="uk-text-bold">quantité négative ou non entière.</span></p> 
                        <hr>
                        <span class="uk-text-bold">Si vous rencontrez un problème merci de me contacter par mail : benhassenm@tutamail.com</span>
                    </div>`);
                    UIkit.scroll(formSubmit).scrollTo("#top");
                    } 
                    else {
                        
                        html = `<p>Vous avez commandé sous le nom de : ` + data['name'] + " - " + data['first_name'] + `
                        <br>L'adresse mail rentrée est : <span class="uk-text-primary">` + data['email'] + `</span><br>
                        <span class="uk-text-bold">Prix total de votre commande : ` + data['total'] + " €</span></p>";

                        delete(data['name']);            
                        delete(data['first_name']);
                        delete(data['email']);
                        delete(data['total']);

                        console.log(data);
                        console.log(html);
                        

                        var n = 0;
                        for (d in data)
                        {
                            n ++;
                        }


                        html += `<table class="uk-table uk-table-divider uk-table-striped uk-table-hover uk-table-middle">
                            <thead>
                                <tr>
                                    <th>Nom du café</th>
                                    <th>Poids commandé</th>
                                    <th>Type de café</th>
                                    <th>Quantité commandé</th>
                                    <th>Prix à payer (en €)</th>
                                </tr>
                            </thead>
                            <tbody>`;
                        for (var i = 0; i < n; i++) {
                            html += "<tr>";
                            for (let index = 0; index < data[i].length; index++) {
                                html += "<td>" + data[i][index] + "</td>";
                            }
                            html += "</tr>";
                        }
                        html += "</tbody></table>";

                        modal.html(html);
                        UIkit.modal("#recap").show();
                    }
                }
            });
        }    
    });

    $("#modalSubmit").click(function(){
        send = true;
        $("#formSubmit").trigger('click');
    });
});
