from django.urls import path
# Импортируем созданное нами представление
from .views import (PostsList, PostDetail, PostCreate, SearchList,
                    PostUpdate, PostDelete, PersonalPage, upgrade_me)
from allauth.account.views import LogoutView, LoginView


urlpatterns = [

   path('', PostsList.as_view(), name='posts_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', SearchList.as_view(), name='post_search'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('articles/create/', PostCreate.as_view(), name='post_create'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
   path('personal/', PersonalPage.as_view(), name='personal_page'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('logout/', LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
]