from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from blog_app.forms import CommentForm
from blog_app.models import Post, PUBLISHED, Comment


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post_list.html'


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
                             slug=slug,
                             status=PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )
    user = request.user
    comments = post.comments.filter(active=True)
    if request.method == 'GET':
        if user.is_authenticated:
            form = CommentForm(initial={'name': user.username, 'email': user.email})
        else:
            form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if user.is_authenticated:
                comment.user = user
                comment.active = True
            comment.save()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments': comments})
