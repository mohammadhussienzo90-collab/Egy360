# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='list'),
    path('test/', views.blog_list_test, name='test'),
    path('debug/', views.debug_blog, name='debug'),
    path('seed-pyramids/', views.seed_pyramid_articles, name='seed-pyramids'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='detail'),
]