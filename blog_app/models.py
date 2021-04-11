from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):

    DRAFT = "draft"
    PUBLISHED = "published"

    STATUS_CHOICES = (
        (DRAFT, "roboczy"),
        (PUBLISHED, "opublikowany")
    )

    title = models.CharField(max_length=128, verbose_name="Tytuł")
    slug = models.SlugField(max_length=128, unique_for_date=True)
    content = models.TextField(verbose_name="Treść")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Autor")
    published = models.DateTimeField(default=timezone.now, verbose_name="Data publikacji")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated = models.DateTimeField(auto_now=True, verbose_name="Data modyfikacji")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.published, self.slug])

    class Meta:
        ordering = ('-published', )
