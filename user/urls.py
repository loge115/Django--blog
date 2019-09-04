from django.urls import path
from user import views
from user.feeds import ALLPostsRssFeed
# 视图函数命名空间
app_name = 'user'
urlpatterns = [
    path('', views.IndexView.as_view(),name='index'),
    #/post/1/
    path('post/<pk>/',views.PostDetailView.as_view(),name='detail'),
    path('archives/<year>/<month>/',views.ArchivesView.as_view(),name='archives'),
    path('category/<pk>/',views.CategoryView.as_view(),name='category'),
    path('tag/<pk>/',views.TagView.as_view(),name = 'tag'),
    path('all/rss/',ALLPostsRssFeed(),name='rss'),
    # path('search/',views.search,name = 'search'),
]