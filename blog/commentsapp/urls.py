from django.urls import path
from . import views


app_name = 'comments'
urlpatterns = [
    path('post/<int:pk>/comment/', views.CommentCreateView.as_view(), name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.CommentUpdateView.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.CommentUpdateView.comment_remove, name='comment_remove'),
]
