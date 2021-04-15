from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from blog_app.models import Post, PUBLISHED


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post_list.html'


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'

class PostDetailView(View):
    def get(self, request, year, month, day, slug):
        post = get_object_or_404(Post,
                                 slug=slug,
                                 status=PUBLISHED,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day,
                                 )
        return render(request, 'blog/post_detail.html', {'post': post})
