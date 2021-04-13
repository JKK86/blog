from django.contrib import admin

from blog_app.models import Post, PUBLISHED


def publish_post(model_admin, request, query_set):
    query_set.update(status=PUBLISHED)


publish_post.short_description = "Opublikuj posty"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'published', 'created', 'updated', 'status']
    list_filter = ['status', 'published', 'created', 'updated', 'author']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ['created', 'updated', 'published']
    list_editable = ['status']
    actions = [publish_post, ]
