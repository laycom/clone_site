from django.db import models



class NewsCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "NewsCategory %s" % self.name


class News(models.Model):
    article = models.CharField(max_length=64)
    text_news = models.TextField()
    descriptions = models.TextField(null=True)
    image = models.ImageField(upload_to='article', null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    link = models.CharField(max_length=64, null=True)

    def __str__(self):
        return "%s" % self.article
