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

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from article.views import home
from django.contrib.flatpages import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", home, {"filtered":"Public"}, name="home"),
    path('admin/', admin.site.urls),
    path('compte/', include("registration.urls")),
    path('article/', include("article.urls")),
    path('evenement/', include("event.urls")),
    path('commande/', include('command.urls')),
    path('a-propos-du-site/', views.flatpage, {'url': "/a-propos-du-site/"}, name="a_propos"),
    path('carousel/', include("carousel.urls")),
    path("cafe/", include("coffee.urls")),
    path('pate/', include("pasta.urls")),
    path('pages/', include('django.contrib.flatpages.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
