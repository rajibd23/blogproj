# from hashlib import md5
#from urllib import urlencode
#from django.utils.http import urlencode

from django import template

register = template.Library()
# #
# #
# # @register.simple_tag
# # def get_gravatar(email, size=60, rating='g', default=None):
# #     """ Return url for a Gravatar. From Zinnia blog. """
# #     url = 'https://secure.gravatar.com/avatar/{0}.jpg'.format(
# #         md5(email.strip().lower()).hexdigest()
# #     )
# #     options = {'s': size, 'r': rating}
# #     if default:
# #         options['d'] = default
# #
# #     url = '%s?%s' % (url, urlencode(options))
# #     return url.replace('&', '&amp;')
# #
# # # def _get_avatars(user):
# # #     # Default set. Needs to be sliced, but that's it. Keep the natural order.
# # #     avatars = user.avatar_set.all()
# # #
# # #     # Current avatar
# # #     primary_avatar = avatars.order_by('-primary')[:1]
# # #     if primary_avatar:
# # #         avatar = primary_avatar[0]
# # #     else:
# # #         avatar = None
# # #
# # #     if settings.AVATAR_MAX_AVATARS_PER_USER == 1:
# # #         avatars = primary_avatar
# # #     else:
# # #         # Slice the default set now that we used
# # #         # the queryset for the primary avatar
# # #         avatars = avatars[:settings.AVATAR_MAX_AVATARS_PER_USER]
# # #     return (avatar, avatars)
# #
@register.simple_tag
def page_query(request, page_num):
    qs = request.GET.copy()
    qs['page'] = page_num
    return qs.urlencode().replace('&', '&amp;')
