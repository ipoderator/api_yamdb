from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, get_jwt_token_for_user, signup

router = DefaultRouter()

users_router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', get_jwt_token_for_user, name='token'),
    path('v1/auth/signup/', signup),
    path('v1/', include(router.urls)),
]
