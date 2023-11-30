from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.filters import TitleFilter
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleGetSerializer,
    TitleSerializer
)
from reviews.models import (
    Category,
    Genre,
    Review,
    Title
)
from users.permissions import (
    IsAdminModeratorAuthorOrReadOnly,
    IsAdminUserOrReadOnly
)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Review model ViewsSet.

    Only authenticated users can add new reviews.
    Users can edit only their own reviews.
    Admins and moders can edit reviews of all users.
    """

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModeratorAuthorOrReadOnly,
    )
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
        'trace'
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Comment model ViewsSet.

    Only authenticated users can add new comments.
    Users can edit only their own comments.
    Admins and moders can edit coments of all users.
    """

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModeratorAuthorOrReadOnly,
    )
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
        'trace'
    )

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            review=get_object_or_404(
                Review,
                pk=self.kwargs['review_id'],
                title=self.kwargs['title_id']
            )
        )


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        IsAdminUserOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name',
    )
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        IsAdminUserOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = (
        'name',
    )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitleSerializer
    permission_classes = (
        IsAdminUserOrReadOnly,
    )
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
        'trace'
    )
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleSerializer
