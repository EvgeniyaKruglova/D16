from django.urls import path
# Импортируем созданное нами представление

from .views import PostsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, CategoryListView, subscribe

from django.views.decorators.cache import cache_page

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', cache_page(60*1)(PostsList.as_view()),name='post_list'),
   path('<int:pk>',cache_page(60*1)(PostDetail.as_view()),name='post_detail'),
   path('search/',PostSearch.as_view(),name='post_search'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   # path('ru', (Index.as_view()), name='index'),

]
