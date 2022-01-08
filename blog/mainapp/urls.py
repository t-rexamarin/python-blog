from django.urls import path
from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.PostsListView.as_view(), name='posts_list'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('drafts/', views.PostsDraftsListView.as_view(), name='posts_drafts_list'),
    path('post/<pk>/publish/', views.PostUpdateView.post_publish, name='post_publish'),
    path('post/<pk>/delete/', views.PostUpdateView.post_delete, name='post_delete'),
    # path('', views.posts_list, name='posts_list'),
    # path('post/new/', views.post_new, name='post_new'),
    # path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    # path('drafts/', views.posts_drafts_list, name='posts_drafts_list'),
    # path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    # path('post/<pk>/delete/', views.post_delete, name='post_delete'),
]
