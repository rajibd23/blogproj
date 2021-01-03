from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post
from django.urls import reverse

class LatestPostsFeed(Feed):
    title = "ElderKonnect blog"
    link = "http://localhost:8000/"
    description = "Latest posts from ElderKonnect."

    def items(self):
        return Post.objects.filter(
            featured=True
        ).order_by('-timestamp')[0:6]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.overview, 30)

    # Only needed if the model has no get_absolute_url method
    # def item_link(self, item):
    #      return reverse("post_detail", args=[item.title.slug])

from django.utils.feedgenerator import Atom1Feed

class AtomSiteNewsFeed(LatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description