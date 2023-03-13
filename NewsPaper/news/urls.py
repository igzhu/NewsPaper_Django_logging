from django.urls import path
from django.views.decorators.cache import cache_page
from .views import PostsList, PostDetails, PostSearch, PostAdd, PostEdit, PostDelete, PostCategoryView
from .views import upgrade_me_to_author, subscribe_to_category

#app_name = 'news'

urlpatterns = [
    path('', cache_page(60*1)(PostsList.as_view())),
    path('<int:pk>', cache_page(60*5)(PostDetails.as_view()), name='post_detail'),
    path('search/', PostSearch.as_view()),
    path('add/', PostAdd.as_view(), name='post_add'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_add'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    #path('login/', PostsList.as_view(), name='login'),
    path('upgrade/', upgrade_me_to_author, name='upgrade'),
    #path('subscribe/', subscribe_to_category, name='subscribe'),
    path('category/<int:pk>/subscribe/', subscribe_to_category, name='subscribe'),
    path('category/<int:pk>/', PostCategoryView.as_view(), name='category'),
]