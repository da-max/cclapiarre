from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from backend.article.models import Article

class StaticViewSitemap(Sitemap):
    protocol = 'https'
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['changelog', 'home']

    def location(self, item):
        return reverse(item)
