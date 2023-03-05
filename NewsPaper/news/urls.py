from django.urls import path
from .views import PostsList, PostDetails, PostSearch, PostAdd, PostEdit, PostDelete
from .views import upgrade_me_to_author

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetails.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view()),
    path('add/', PostAdd.as_view(), name='post_add'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_add'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    #path('login/', PostsList.as_view(), name='login'),
    path('upgrade/', upgrade_me_to_author, name='upgrade'),
]