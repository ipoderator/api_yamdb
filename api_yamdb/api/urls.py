from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet
)

router_v1 = routers.DefaultRouter()

router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genre', GenreViewSet, basename='genres')
router_v1.register(r'title', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', 
    ReviewViewSet, 
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>/d+)/comments', 
    CommentViewSet, 
    basename='comments'
)


app_name = 'api-v1'

urlpatterns = [
    
]
