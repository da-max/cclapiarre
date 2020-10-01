from django.shortcuts import render
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, HttpResponse
from django.dispatch.dispatcher import receiver
import copy

from django.views.generic import ListView
from django.contrib.auth.views import LogoutView, PasswordChangeView,\
	PasswordChangeDoneView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from rest_framework import permissions

from registration.models import Information
from registration.forms import ConnectionForm, CourtCircuitConnectionForm



class ListUser(PermissionRequiredMixin, LoginRequiredMixin, ListView):

	permission_required = "registration.view_information"
	model = Information
	context_object_name = "information"
	template_name = "registration/list.html"

	def get_queryset(self):

		return Information.objects.all().order_by("user__last_name")



class ResetPassword(PasswordResetView):
	''' Generic view for reset password.
    
    template_name -- This class use registration/password_reset_form.html for display form
    email_template_name -- This class use email/password_reset_email.html for send mail
    subject_template_name -- This class use email/password_reset_subject.txt for display subject of mail.
    success_url -- This class redirect to home after mail send
    
    
	'''

	template_name = 'registration/password_reset.html'
	email_template_name = 'email/password_reset_email.html'
	subject_template_name = 'email/password_reset_subject.txt'
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		''' If form is valid, send message for warn user.
		
		If email send by user is not found in daatbase, display message for warn
		and redirect to reset_password page.
		Else display success message.
		'''
		try:
			User.objects.get(email=form.cleaned_data['email'])
	
		except:
			messages.warning(self.request, "Adresse mail non trouvé, merci de réessayer.")
			return HttpResponseRedirect(reverse_lazy('reset_password'))		
	
		else:
	
			messages.success(self.request, "Un mail vous a été envoyé avec la procédure à suivre afin de réinitialiser votre mot de passe.")
		
		return super().form_valid(form)


	def form_invalid(self, form):
		''' If form is invalid, send message.'''
		messages.warning(self.request, "L'adresse mail rentrée n'est pas conforme, merci de réessayer.")
		return super().form_invalid(form)



class ResetPasswordConfirm(PasswordResetConfirmView):
	''' Generic class for confirm and change password.
 
	template_name -- This class use registration/password_confirm_reset.html for display form for change password.
	success_url -- Then user has change here password, he is redirect to connection page.
 
 
 	'''

	template_name = 'registration/password_confirm_reset.html'
	success_url = reverse_lazy('connection')

	def form_valid(self, form):
		''' If form is valid, send message.'''
		messages.success(self.request, "Votre mot de passe a bien été modifié, vous pouvez à présent vous connecter avec ce dernier.")
		return super().form_valid(form)

	def form_invalid(self, form):
		''' If form is invalid. '''
		messages.warning(self.request, "Votre mot de passe n'a pas pu être modifié, merci de vérifier qu'il respecte bien les critères requis puis réessayer.")
		return super().form_invalid(form)



def connection(request):
	error = False
	connect = False
 
	print(request.method)
	if request.method == "POST":
		
		if request.GET and (request.GET['next'] == "/cafe/commander-du-cafe" or request.GET['next'] == '/pate/commander-des-pates'):
			form = CourtCircuitConnectionForm(request.POST)
		else:
			form = ConnectionForm(request.POST)
		
		
		if form.is_valid():

			if request.GET and (request.GET['next'] == "/cafe/commander-du-cafe" or request.GET['next'] == '/pate/commander-des-pates'):
				username = 'court-circuit'
			else:
				username = form.cleaned_data['username']
		
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)

			if "next" in request.GET:
				next = request.GET["next"]
			else:
				next = "/"

			if user:
				login(request, user)
				return HttpResponseRedirect(next)

			else:
				error = True
	
	elif request.GET and (request.GET['next'] == "/cafe/commander-du-cafe" or request.GET['next'] == '/pate/commander-des-pates'):
		
		form = CourtCircuitConnectionForm()

	else:
		form = ConnectionForm()


	return render(request, "registration/connection.html", locals())


class disconnection(LogoutView):
	next_page = "home"


@receiver(user_logged_in)
def connect(request, user, **kwargs):
	return HttpResponse(messages.success(request, "Bienvenue " + user.username + " !!"))


@receiver(user_logged_out)
def disconnect(request, user, **kwargs):
	return HttpResponse(messages.warning(request, "Au revoir " + user.username + "  et merci d'être passé.e!!"))


class ChangePassword(PermissionRequiredMixin, PasswordChangeView):
	permission_required = "auth.can_change_password"
	template_name = "registration/change_password.html"
	success_url = reverse_lazy('change_password_success')

	def form_invalid(self, form):
		message = messages.warning(self.request, "Une erreur s'est produite. Merci de vérifier que votre ancien mot de passe est juste,<br>\
		de plus, votre nouveau mot de passe doit faire au moins 8 caractères, merci de réctifier puis de ré-essayer")
		return HttpResponseRedirect(reverse_lazy('change_password'), {"form": form})



class ChangePasswordSuccess(PasswordChangeDoneView):
	template_name = "registration/change_password_success.html"


class CustomDjangoModelPermission(permissions.DjangoModelPermissions):

    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)  # from EunChong's answer
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']