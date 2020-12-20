from django.urls import include, path
from knowledge.views import(
knowledge_index,
knowledge_list,
knowledge_thread,
knowledge_moderate,
knowledge_ask,
)

urlpatterns = [
    path('', knowledge_index, name='knowledge_index'),
    path('questions/', knowledge_list, name='knowledge_list'),
    path('questions/<category_slug>/', knowledge_list, name='knowledge_list_category'),
    path('questions/<question_id>/',
        knowledge_thread, name='knowledge_thread_no_slug'),
    path('questions/<question_id>/<slug>/',
        knowledge_thread, name='knowledge_thread'),
    path('moderate/<model>/<lookup_id>/<mod>/',
        knowledge_moderate, name='knowledge_moderate'),
    path('ask/', knowledge_ask, name='knowledge_ask'),
]
