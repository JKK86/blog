from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView
from taggit.models import Tag
from django.db.models import Count

from blog_app.forms import CommentForm, PostShareForm, SearchForm
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
    tag_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__id__in=tag_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]
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
    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'form': form,
                                                     'similar_posts': similar_posts,
                                                     'comments': comments})


class PostShareView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = PostShareForm()
        sent = False
        return render(request, 'blog/post_share.html', {'post': post, 'form': form, 'sent': sent})

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = PostShareForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            comment = form.cleaned_data['comment']
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{name} poleca post {post.title}"
            message = f"Zachęcam do  przeczytania posta {post.title} na stronie {post_url} \nKomentarz od {name}: " \
                      f"{comment}"
            email_from = form.cleaned_data['email_from']
            email_to = form.cleaned_data['email_to']
            send_mail(subject, message, email_from, [email_to])
            sent = True
            return render(request, 'blog/post_share.html', {'post': post, 'form': form, 'sent': sent})


class PostSearchView(View):
    def get(self, request):
        form = SearchForm()
        query = None
        results = []
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                # search_vector = SearchVector('title', weight='A') +\
                #                 SearchVector('content', weight='B')
                # search_query = SearchQuery(query)
                # results = Post.published.annotate(
                #     search=search_vector,
                #     rank=SearchRank(search_vector, search_query)
                # ).filter(rank__gte=0.3).order_by("-rank")
                results = Post.published.annotate(
                    similarity=TrigramSimilarity('title', query),
                ).filter(similarity__gt=0.1).order_by('-similarity')
        return render(request, 'blog/search.html', {'form': form, 'query': query, 'results': results})
