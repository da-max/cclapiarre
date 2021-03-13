from django.urls import reverse_lazy
from django.forms import models, TextInput, Textarea, DateField
from django.forms.widgets import DateTimeInput, Select, SelectDateWidget
from django.forms.forms import Form
from django.forms.fields import CharField
from django.core.mail import send_mail

from django.contrib import messages

from backend.event.models import Event

class EventForm(models.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            "date": DateTimeInput(attrs={"class" : "uk-input"}),
            "title": TextInput(attrs={"class" : "uk-input"}),
            "description": Textarea(attrs={"class" : 'uk-textarea'})
        }

"""class DateLimitUserForm(models.ModelForm):
    class Meta:
        model = DateLimitUser
        fields = ("date",)
        widgets = {
            "date" : SelectDateWidget(attrs={"class": "uk-select uk-select-small uk-form-width-medium uk-margin-small-right"})
        }

class MailForm(Form):
    recipient = CharField(max_length=200, label="Destinataires du message")
    subject = CharField(max_length=200, label="Objet du message")
    message = CharField(label="Message :")

    recipient.widget = TextInput(attrs={"class" : "uk-input"})
    subject.widget = TextInput(attrs={"class" : "uk-input"})
    message.widget = Textarea(attrs={"class" : 'uk-textarea', "id": "message"})

    def send_mail(self, request):
        recipient = self.recipient
        subject = self.subject
        message = self.message

        send_mail(subject, message, "cclapiarre@alwaysdata.net", recipient)"""
