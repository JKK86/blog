from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from blog_app.models import Post, PUBLISHED


class PostListView(ListView):
    queryset = Post.objects.filter(status=PUBLISHED)
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post_list.html'
