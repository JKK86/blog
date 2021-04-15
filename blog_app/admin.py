from django.contrib import admin

from blog_app.models import Post, PUBLISHED, Comment


def publish_post(model_admin, request, query_set):
    query_set.update(status=PUBLISHED)


publish_post.short_description = "Opublikuj posty"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'created', 'updated', 'status']
    list_filter = ['status', 'publish', 'created', 'updated', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ['created', 'updated', ]
    list_editable = ['status']
    actions = [publish_post, ]
    ordering = ['status', '-publish']
    date_hierarchy = 'publish'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'text', 'user', 'created', 'active']
    list_filter = ['user']
    search_fields = ['text']
    exclude = ['created', 'updated']
    list_editable = ['active']
    ordering = ['-created']
