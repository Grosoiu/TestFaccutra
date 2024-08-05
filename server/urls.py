from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.signup),
    path('login', views.login),
    path('test_token', views.test_token),
    path("edit_permissions/<int:user_id>", views.UserUpdateView.as_view()),
]
