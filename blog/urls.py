# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='list'),
    path('test/', views.blog_list_test, name='test'),
    path('debug/', views.debug_blog, name='debug'),
    path('seed-pyramids/', views.seed_pyramid_articles, name='seed-pyramids'),
    path('seed-rich/', views.seed_rich_articles, name='seed-rich'),
    path('seed-attractions/', views.seed_attractions, name='seed-attractions'),
    path('seed-new-articles/', views.seed_new_articles, name='seed-new-articles'),
    path('deploy-check/', views.deploy_check, name='deploy-check'),

    # SEO Pillar Pages - High-value landing pages
    path('egypt-travel-guide/', views.pillar_egypt_guide, name='egypt_guide'),

    # Article detail (must be last due to slug pattern)
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='detail'),
]