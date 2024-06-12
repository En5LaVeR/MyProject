from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostCreate, SearchList


urlpatterns = [

   path('', PostsList.as_view(), name='posts_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', SearchList.as_view(), name='post_search'),
   path('create/', PostCreate.as_view(), name='post_create')
]