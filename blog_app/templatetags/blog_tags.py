from django import template

from blog_app.models import Post

register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()