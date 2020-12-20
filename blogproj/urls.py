from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from allauth.account import views as allauth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

#from allauth.account import views
from post.views import (
    index,
    search,
    post_list,
    tagged_post_list,
    post_detail,
    post_create,
    post_update,
    post_delete,
    IndexView,
    likePost,
   # login,
   # logout,
   # signup,
    SearchView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from marketing.views import email_list_signup

from blog.views import get_user_profile, user_profile_update, avatar_update

urlpatterns = [

    path('admin/', admin.site.urls),
    # path('', index),
    path('', IndexView.as_view(), name='home'),
    #path('post_list/', post_list, name='post-list'),
    path('blog/', PostListView.as_view(), name='post-list'),
    #path('search/', search, name='search'),
    path('search/', SearchView.as_view(), name='search'),
    path('email-signup/', email_list_signup, name='email-list-signup'),
    #path('create/', post_create, name='post-create'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('post/<pk>/', post_detail, name='post-detail'),
    #path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    #path('post/<pk>/update/', post_update, name='post-update'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<pk>/delete/', post_delete, name='post-delete'),

    #path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('tinymce/', include('tinymce.urls')),

    path(
            'accounts/password/change/',
            login_required(
                allauth_views.PasswordChangeView.as_view(
                    success_url=reverse_lazy('account_login')
                )
            ),
            name='account_change_password'
        ),

    path('accounts/', include('allauth.urls')),
    path('knowledge/', include('knowledge.urls')),
    path('avatar/', include('avatar.urls')),

    path('profile/<username>', get_user_profile, name='profile-home'),
    path('update_avatar/<username>', avatar_update, name='update-avatar'),
    path('update_profile/<username>', user_profile_update, name='update-profile'),

    #path('identity/<pk>', ProfileIdentite.as_view(), name='profile-identity-form'),
    path('likepost/<pk>', likePost, name='likepost'),   # likepost view at /likepost
    path('tag/<tag_slug>', tagged_post_list, name='post_list_by_tag'),


    # path("signup/", signup, name="blog_signup"),
    # path("login/", login, name="blog_login"),
    #
    # path("logout/", logout, name="blog_logout"),
    # path(
    #     "password/change/",
    #     views.password_change,
    #     name="account_change_password",
    # ),
    # path("password/set/", views.password_set, name="account_set_password"),
    # path("inactive/", views.account_inactive, name="account_inactive"),
    # # E-mail
    # path("email/", views.email, name="account_email"),
    # path(
    #     "confirm-email/",
    #     views.email_verification_sent,
    #     name="account_email_verification_sent",
    # ),
    # re_path(
    #     r"^confirm-email/(?P<key>[-:\w]+)/$",
    #     views.confirm_email,
    #     name="account_confirm_email",
    # ),
    # # password reset
    # path("password/reset/", views.password_reset, name="account_reset_password"),
    # path(
    #     "password/reset/done/",
    #     views.password_reset_done,
    #     name="account_reset_password_done",
    # ),
    # re_path(
    #     r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
    #     views.password_reset_from_key,
    #     name="account_reset_password_from_key",
    # ),
    # path(
    #     "password/reset/key/done/",
    #     views.password_reset_from_key_done,
    #     name="account_reset_password_from_key_done",
    # ),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
