from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from kays.models import Post
# from kays.models import Tag

class StaticSitemap(Sitemap):
    def items(self):
        return ['index', 'about', 'contact', 'gallery', 'rooms', 'services', 'booking']
    
    def location(self,item):
        return reverse(item)

class PostViewSitemap(Sitemap):
    def items(self):
        return Post.objects.all()[:100]
    
    
# class CategorySitemap(Sitemap):
#     def items(self):
#         return Tag.objects.all()