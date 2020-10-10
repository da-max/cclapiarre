from django.conf.urls import url
from django.urls import path

from backend.pasta.views import pdf_list_command, pdf_global_command, list_command ,get_pasta_list, command_pasta, new_command, global_command

urlpatterns = [
    url(r'^liste-des-commandes$', list_command, name='pasta_list_command'),
    url(r'^get-products$', get_pasta_list),
    url(r'^commander-des-pates', command_pasta, name="pasta_command"),
    url(r'^create-command$', new_command),
    url(r'^commande-globale$', global_command, name='pasta_global_command'),
    url(r'^pdf-liste-des-commandes', pdf_list_command, name='pasta_pdf_list_command'),
    url(r'^pdf-commande-globale', pdf_global_command, name='pasta_pdf_global_command')
]
