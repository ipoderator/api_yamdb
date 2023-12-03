from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.filters import TitleFilter
from api.mixins import ListCreateDestroyViewSet
from api.permissions import (
    IsAdminUserOrReadOnly,
    IsAdminModeratorAuthorOrReadOnly,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleGetSerializer,
    TitleSerializer,
)
from api.utils import HTTPMethods
from reviews.models import (
    Category,
    Genre,
    Review,
    Title,
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

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


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

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(
                Review,
                pk=self.kwargs['review_id'],
                title=self.kwargs['title_id']
            )
        )


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    Category model ViewsSet.

    Only the administrator can retrieve the data.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        IsAdminUserOrReadOnly,
    )
    filter_backends = (
        filters.SearchFilter,
    )


class GenreViewSet(ListCreateDestroyViewSet):
    """
    Genre model ViewSet.

    Only the administrator can retrieve the data.
    The search is by name.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        IsAdminUserOrReadOnly,
    )
    filter_backends = (
        filters.SearchFilter,
    )
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Title model ViewSet.

    We calculate the average rating and sort by name.
    We did this so that there would be equal paganation.
    Only the administrator can retrieve the data.
    """

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (
        IsAdminUserOrReadOnly,
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == HTTPMethods.GET:
            return TitleGetSerializer
        return TitleSerializer
