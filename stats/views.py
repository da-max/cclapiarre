from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages

from stats.models import PageAccess
from stats.forms import PageAccessForm


class ListPageAccess(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ This class is use for display list of PageAccess objects

    Extends:
        LoginRequiredMixin -- This view is accessible if the user is connect
        PermissionRequiredMixin -- Ths ciew require permission (specified with permission_required attribute)
        ListView -- This class extend to generic class ListView

    Attributes:
        permission_required -- This view is display is user have stats.view_pageaccess permission.
        model -- This class use PageAccess model.
        context_object_name -- The name of object_name (use in template for because this attribute contains object) is pages.
        template_name -- The data is send to stats/page_access/list.html template.
    """

    permission_required = 'stats.view_pagesaccess'
    model = PageAccess
    context_object_name = 'pages'
    template_name = 'stats/page_access/list.html'
    queryset = PageAccess.objects.all()


class CreatePageAccess(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Generic class for create PageAccess object.

    Extends:
        LoginRequiredMixin -- This view is accesible if the user is connect
        PermissionRequiredMixin -- This view require permission 
        CreateView -- This class extends to genric view CreateView.

    Attributes:
        permissions_required -- This view is diplay is user have stats.create_pageaccess permission
        model -- This class use PageAccess
        template_name -- The data is send to stats/page_access/new.html template for display form.
        success_url --- If the data send for create PageAcces are just, the user is redirect to list_pageaccess view.
        form_class --- This class use PageAccessForm class for display formm.
    """

    permission_required = 'stats.create_pageaccess'
    model = PageAccess
    template_name = 'stats/page_access/new.html'
    success_url = reverse_lazy('list_pageaccess')
    form_class = PageAccessForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        messages.success(self.request, "La règle a bien été enregistrée.")
        return HttpResponseRedirect(self.get_success_url())
    
    