from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView


from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin,\
	LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required


from event.models import Event
from carousel.models import Carousel
from article.forms import ArticleForm
from article.models import Article



class ListArticle(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Generic class for list article is extends to ListView.

    permission_required -- User with permission view_article can view this page.
    model -- This class use Article model.
    context_object_name -- This class use articles for templates.
    template_name -- This class take list.html template.

    get_queryset -- Method for select article.
    

    """
    
    permission_required = "article.view_article"
    model = Article
    context_object_name = "articles"
    template_name = "article/list.html"


    def get_queryset(self):
        """ Method for select all articles and rank 
        them according to their date of creation.
        
        
        """
        return Article.objects.all().order_by("-date_creation")



class CreateArticle(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Generic class for create an article.
    
    permission_required -- User with permission add_article can view this page.
    model -- This class use Article model .
    template_name -- This class take new.html template.
    form_class -- This class use ArticleForm class for form.
    success_url -- Success url is list of article (ListArticle class).

    form_valid -- If form is valid.
    form_invalid -- If form is invalid.

    """
    
    permission_required = "article.add_article"
    model = Article
    template_name = "article/new.html"
    form_class = ArticleForm
    success_url = reverse_lazy("list_article")


    def form_valid(self, form):
        """ If form is valid, article is save, and author is user.
        This method use messages system for warner user.
        
        
        """
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        messages.success(self.request, "Votre article a bien été enregistré.")
        return HttpResponseRedirect(self.get_success_url())


    def form_invalid(self, form):
        """If form is invalid : 
        This method use messages for warner user, and redirect to
        create article page with form complete.
        
        
        """
        messages.warning(self.request, "Votre article n'a pas pu être enregistré, merci de verifier que vous avez remplis tout les champs, puis réessyaer.")
        return HttpResponseRedirect(reverse_lazy("create_article"), {"form":form})



class UpdateArticle(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Generic class for update an article.
    
    permission_required -- Users with permission change_aritcle can view this page.
    model -- This class use Article model.
    template_name -- It use update.html template.
    content_object_name -- article is name of variable for display articles in template.
    success_url -- Success_url is list of articles (ListArticle class).
    form_class -- ArticleFom is Class for form.
    
    
    """
    
    permission_required = "article.change_article"
    model = Article
    template_name = "article/update.html"
    content_object_name = "article"
    success_url = reverse_lazy('list_article')
    form_class = ArticleForm


    def get_object(self, queryset=None):
        """ This method take article from id.
        
        Key word Arguments:
            queryset {int} -- [id of article for take in database.] (default: {None})
        
        Return:
            [Article or 404] -- [Article object for display in update template.]
        

        """
        id = self.kwargs.get("id_article", None)
        return get_object_or_404(Article, id=id)


    def form_valid(self, form):
        """ If form is valid.
        
        Arguments:
            form {ArticleForm} -- [Form that the user has send.]
        
        Return:
            [HttpResponse] -- [redirect to success_url.]


        """
        self.object = form.save()
        messages.success(self.request, "Votre article a bien été modifié.")
        return HttpResponseRedirect(self.get_success_url())


    def form_invalid(self, form):
        """ If form is invalid
        
        Arguments:
            form {ArticleForm} -- [Form that the user has send.]
        
        Return:
            [HttpResponse] -- [Redirect to update article page, with form and warning message.]


        """
        messages.warning(self.request, "Votre article n'a pas pu être enregistré, merci de verifier que vous avez remplis tout les champs, puis réessyaer.")
        id_article = self.kwargs.get("id_article", None)
        return HttpResponseRedirect(reverse_lazy("update_article", kwargs={"id_article":id_article}), {"form":form})



def home(request, filtered):
    """ Home of site.
    
    Arguments:
        request {request} -- [Request with Http information.]
        filtered {string} -- [String for filtered article with categorie name.]
        

    """
    event = Event.objects.all().order_by("date")
    article = Article.objects.filter(categorie__name=filtered).order_by("-date_creation")
    carousels = Carousel.objects.all().order_by('position')
    return render(request, "article/home.html", locals())



@login_required
@permission_required("article.delete_article", raise_exception=True)
def delete_article(request, id):
    """ For delete an article
    
    Arguments:
        request {request} -- [Request with Http informations.]
        id {int} -- [id of article.]
    
    Return:
        [HttpResponse] -- [Redirect to list of article.]

    
    """
    article = get_object_or_404(Article, id=id)
    result = article.delete()
    success_url = reverse_lazy("list_article")

    if result:
        messages.success(request, "Votre article a bien été supprimé.")

    else:
        messages.warning(request, "Votre article n'a pas pu être modifié.")

    return HttpResponseRedirect(success_url)


