"""cclapiarre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.i18n import JavaScriptCatalog


from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.contrib.flatpages import views
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView
from graphql_jwt.decorators import jwt_cookie


from backend.article import views as a_views
from backend.article.sitemaps import StaticViewSitemap
from backend.api.apps import ApiConfig


sitemaps = {
    'static': StaticViewSitemap(),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('compte/', include("backend.registration.urls")),
    path('article/', include("backend.article.urls")),
    path('evenement/', include("backend.event.urls")),
    path('agrumes/', include(('backend.citrus.urls', 'citrus'), namespace='citrus')),
    path('a-propos-du-site/', views.flatpage,
         {'url': "/a-propos-du-site/"}, name="a_propos"),
    path('carousel/', include("backend.carousel.urls")),
    path("cafe/", include("backend.coffee.urls")),
    path('pate/', include("backend.pasta.urls")),
    path('parametre/', include('backend.stats.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),

    # Page for display content of CHANGELOG.md files
    path('changements', a_views.changelog, name='changelog'),

    # Api
    url(r'^api/', include(('backend.api.urls', 'api'), namespace='api')),

    path('jsi18n', JavaScriptCatalog.as_view(), name='javascript-catalog'),

    # Utility
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    url(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt",
                                              content_type="text/plain"), name="robots_file"),

    path('graphql/', jwt_cookie(GraphQLView.as_view(graphiql=True))),
    url(r'/*', TemplateView.as_view(template_name='app.html'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
