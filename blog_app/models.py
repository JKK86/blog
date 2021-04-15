from django.db import models
from django.urls import reverse
from django.utils import timezone

from blog import settings

DRAFT = "draft"
PUBLISHED = "published"


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=PUBLISHED)


class Post(models.Model):

    STATUS_CHOICES = (
        (DRAFT, "roboczy"),
        (PUBLISHED, "opublikowany")
    )

    title = models.CharField(max_length=128, verbose_name="Tytuł")
    slug = models.SlugField(max_length=128, unique_for_date='publish')
    content = models.TextField(verbose_name="Treść")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts',
                               verbose_name="Autor")
    publish = models.DateTimeField(default=timezone.now, verbose_name="Data publikacji")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated = models.DateTimeField(auto_now=True, verbose_name="Data modyfikacji")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    class Meta:
        ordering = ('-publish', )