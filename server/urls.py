from django.urls import re_path
from django.urls import path

from . import views

urlpatterns = [
    re_path('signup', views.signup),
    re_path('login', views.login),
    re_path('test_token', views.test_token),
    re_path('^company$', views.company), # FOARTE IMPORTANT!! ^$ puse pentru ca regex lua si endpointul de mai jos
    re_path(r'user/(?P<column_name>\w+)', views.update_user_column),
    re_path(r'company/(?P<company_id>\d+)/(?P<column_name>\w+)', views.update_company_column),
    # path('company/<int:company_id>/<str:column_name>/', views.update_company_column),
]
