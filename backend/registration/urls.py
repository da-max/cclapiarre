from django.urls import path, re_path
from django.conf.urls import url

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout_then_login

from backend.registration.views import ChangePassword, ChangePasswordSuccess, disconnection, connection, ListUser, ResetPassword, ResetPasswordConfirm

urlpatterns = [
	path('connexion', connection , name="connection"),
	path('disconnection', disconnection.as_view(), name="disconnection"),
	path('changer-son-mot-de-passe', ChangePassword.as_view(), name='change_password'),
	path('changer-utilisateur', logout_then_login, name="disconnection_connection"),
	path("changement-mot-de-passe-reussi", ChangePasswordSuccess.as_view(), name="change_password_success"),
	path('liste-des-adhérents', ListUser.as_view(), name="list_user"),
	re_path(r'^reinitialiser-son-mot-de-passe', ResetPassword.as_view(), name='reset_password'),
	url(r"^nouveau-mot-de-passe?uidb64=(?P<uidb64>[0-9A-Za-z_\-]+)&token=(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$", ResetPasswordConfirm.as_view(), name='password_reset_confirm'),
]
