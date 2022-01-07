from django.urls import path
from django.contrib.auth import views
from .views import LoginListView


app_name = 'authapp'
urlpatterns = [
    path('login/', LoginListView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='/'), name='logout'),

]
