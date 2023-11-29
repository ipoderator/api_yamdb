from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet
)
from users.views import UserViewSet, get_jwt_token_for_user, signup

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(
    r'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    r'genre',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    r'title',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    'review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    'comment'
)
router_v1.register(
    r'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/auth/token/', get_jwt_token_for_user, name='token'),
    path('v1/auth/signup/', signup),
    path('v1/', include(router_v1.urls)),
]
