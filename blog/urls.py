from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import url
#from post import views
from post.views import (
    index,
    search,
    post_list,
    post_detail,
    post_create,
    post_update,
    post_delete,
    IndexView,
    SearchView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from marketing.views import email_list_signup

app_name = 'blog'
urlpatterns = [

    # path('', index),
    path('', IndexView.as_view(), name='home'),
    # path('blog/', post_list, name='post-list'),
    #path('post_list/', PostListView.as_view(), name='post-list'),
    #path('search/', search, name='search'),
    #path('search/', SearchView.as_view(), name='search'),
    path('email-signup/', email_list_signup, name='email-list-signup'),
    # path('create/', post_create, name='post-create'),
    #path('create/', PostCreateView.as_view(), name='post-create'),
    # path('post/<id>/', post_detail, name='post-detail'),
    path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/<id>/update/', post_update, name='post-update'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<id>/delete/', post_delete, name='post-delete'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    #
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
