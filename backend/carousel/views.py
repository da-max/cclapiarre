from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView
from django.urls.base import reverse_lazy

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin,\
    LoginRequiredMixin

from backend.carousel.models import Carousel
from backend.carousel.forms import CarouselForm


class ListCarousel(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    ''' Generic class for list carousel.

    permission_required -- User with permission view_carousel can view this page.
    model -- This class use carousel model.
    context_object_name -- carousels is name of variable for diplay carousels.
    template_name -- It use list.html template.


    '''

    permission_required = "carousel.view_carousel"
    model = Carousel
    context_object_name = "carousels"
    template_name = "carousel/list.html"


class UpdateCarousel(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    ''' Generic class for update a carousel.

    permission_required -- Users with permissions update_carousel can view this page.
    model -- This class use Carousel model.
    context_object_name -- carousel is name of variable for display carousel in form.


    '''

    permission_required = "carousel.update_carousel"
    model = Carousel
    context_object_name = 'carousel'
    template_name = "carousel/update.html"
    success_url = reverse_lazy('list_carousel')
    form_class = CarouselForm

    def get_object(self, queryset=None):
        id = self.kwargs.get('id_carousel', None)
        return get_object_or_404(Carousel, id=id)

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Le carousel a bien été modifié.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.warning(
            self.request, "Votre carousel n'a pas pu être enregistré, merci de réessayer.")
        id_carousel = self.kwargs.get("id_carousel", None)
        return HttpResponseRedirect(reverse_lazy('update_carousel', kwargs={"id_carousel": id_carousel}), {"form": form})


class CreateCarousel(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    ''' Generic class for create a carousel.

    permission_required -- Users with permissions add_carousel can view this page.
    model -- This class use Carousel model.
    form_class -- This class use CarouselForm for display form/
    success_url -- If form_isvalid, the user is redirect to carousel_list view.


    '''

    permission_required = "carousel.add_carousel"
    model = Carousel
    template_name = "carousel/new.html"
    form_class = CarouselForm
    success_url = reverse_lazy('list_carousel')

    def form_invalid(self, form):
        ''' If form is invalid, this function is call
        and send messages for warn user.

        '''

        messages.warning(
            self.request, "Votre carousel n'a pas pu être enregistré, merci de réessayer.")
        return HttpResponseRedirect(reverse_lazy('create_carousel'), {"form": form})

    def form_valid(self, form):
        ''' If form is valid, this function is call. Save the carousel,
         send a message of success and redirect user to list of carousel.

        '''

        self.object = form.save()
        messages.success(self.request, "Votre carousel a bien été enregistré.")
        return HttpResponseRedirect(self.get_success_url())


def delete_carousel(request, id_carousel):
    ''' This function is call when an user wants delete a carousel.

    carousel -- Object get with id switch to parametres or raise a 404 error.
    result -- Reply of delete carousel.
    success_url -- Redirect user to list of carousel.

    The message depent on the answer of carousel.delete()

    '''

    carousel = get_object_or_404(Carousel, id=id_carousel)
    result = carousel.delete()
    success_url = reverse_lazy('list_carousel')

    if result:
        messages.success(request, "Le carousel a bien été supprimé.")
    else:
        messages.warning(
            request, "Le carousel n'a pas pu être supprimé, merci de réessayer.")

    return HttpResponseRedirect(success_url)
