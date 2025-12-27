# reviews/urls.py
from django.urls import path
from . import web_views

app_name = 'reviews'

urlpatterns = [
    path('submit/<str:item_type>/<int:item_id>/', web_views.submit_review, name='submit'),
    path('<int:review_id>/vote/', web_views.vote_helpful, name='vote'),
    path('<int:review_id>/report/', web_views.report_review, name='report'),
]