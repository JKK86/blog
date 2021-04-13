from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from blog_app.models import Post, PUBLISHED


class PostListView(View):
    def get(self, request):
        posts = Post.objects.filter(status=PUBLISHED)
        return render(request, 'blog/post_list.html', {'posts': posts})


# class PostListView2(ListView):
