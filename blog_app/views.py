from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView
from taggit.models import Tag

from blog_app.forms import CommentForm
from blog_app.models import Post, PUBLISHED, Comment

User = get_user_model()

# Widok oparty na widoku generycznym ListView
# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 5
#     template_name = 'blog/post_list.html'


class PostListView(View):
    def get(self, request, tag_slug=None):
        post_list = Post.published.all()
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            post_list = post_list.filter(tags__in=[tag])
        paginator = Paginator(post_list, 5)
        page = request.GET.get('page', 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request, 'blog/post_list.html', {
            'posts': posts, 'tag': tag, 'page': page
            })


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
            else:
                messages.info(request,
                              "Twój komentarz oczekuje na zatwierdzenie. "
                              "Zaloguj się jeśli chcesz, aby Twoje komentarze były publikowane bez zwłoki.")
                subject = 'Komentarz do zatwierdzenia'
                message = render_to_string('blog/approve_comment_email.html', {
                    'name': form.cleaned_data['name'],
                    'email': form.cleaned_data['email'],
                    'post': post
                })
                email_from = 'my_blog@local.com'
                email_to = [user.email for user in User.objects.filter(is_staff=True)]
                send_mail(subject, message, email_from, email_to, fail_silently=False)
            comment.save()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments': comments})
