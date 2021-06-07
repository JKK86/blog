from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from blog_app.models import Post


class LatestPostFeed(Feed):
    title = "Mój blog"
    link = ""
    description = "Nowe posty na blogu"

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)
