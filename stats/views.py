from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
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
        """ Method call when the form is valid. Save the data in database.

        Arguments:
            form {cleanned_data} -- Data cleanned after verification

        Returns:
            Response -- Redirect to list_pageaccess when the rules is save.
        """
        self.object = form.save()
        messages.success(self.request, "La règle a bien été enregistrée.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """ Method for define comportement when an user send bad data

        Arguments:
            form {cleanned_data} -- Cleanned_data after automatic verification

        Returns:
            Response -- contains warning messages and form.
        """
        messages.warning(self.request, "La règle n’a pas pu être enregistré, merci de vérifier que \
        tous les champs ont bien été remplis, puis réessayer.")
        return HttpResponseRedirect(reverse_lazy('create_pageaccess', {'form': form}))


class UpdatePageAccess(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Class for update pageaccess

    Extends:
        LoginRequiredMixin -- This view required login user.
        PermissionRequiredMixin -- This view required permission for access to view.
        UpdateView  -- This class extends to UpdateView.

    Attribute:
        permission_required -- The view is accessible if user have stats.change_pageaccess permission
        model -- This view use PageAccess model.
        template_name -- The template for this view is stats/page_access/update.html
        success_url -- If form is valid, the user is redirect to list_pageaccess (ListPageAccess class)
        form_class -- The form is PageAccessForm (display in template)
    """
    permission_required = "stats.change_pageaccess"
    model = PageAccess
    template_name = "stats/page_access/update.html"
    content_object_name = 'page_access'
    success_url = reverse_lazy('list_pageaccess')
    form_class = PageAccessForm

    def get_object(self):
        """ Method for define rules for get_object

        Returns:
            PageAccess or 404 -- If object is find with id (define in url), an object is return, else raise 404 error. 
        """
        id = self.kwargs.get('id_pageaccess', None)
        return get_object_or_404(PageAccess, id=id)
    
    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "La règle <span class='uk-text-italic'>« {} »</span> a bien été modifiée.".format(self.object.name))
        return HttpResponseRedirect(self.get_success_url())