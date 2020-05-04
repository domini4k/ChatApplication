from django.urls import path, re_path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view),
    path('register/', views.register_view),
    path('logout/', views.logout_view),
    path ('', views.start_page),
    re_path(r'accounts/login/.*', views.start_page)
    ]
