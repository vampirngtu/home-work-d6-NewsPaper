from django.urls import path
from .views import NewsList, NewDetail, Search, PostAdd, PostEdit, PostDelete, become_author, CategoryList, CategoryDetali, subscribe, unsubscribe
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(NewsList.as_view())),
    path('<int:pk>/', NewDetail.as_view(), name='new'),
    path('search/', Search.as_view()),
    path('add/', PostAdd.as_view(), name='add'),
    path('<int:pk>/edit/',PostEdit.as_view(), name='new_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='new_delete'),
    path('become_author/',become_author,name = "become_author"),
    path('categories/', CategoryList.as_view(), name='categories'),
    path('categories/<int:pk>', CategoryDetali.as_view(), name='category'),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name='unsubscribe'),
    
    
] 