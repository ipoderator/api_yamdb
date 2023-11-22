from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from .serializers import ReviewSerializer
from reviews.models import Title


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Review model ViewsSet.

    Only authenticated users can add new reviews.
    Users can edit only their own reviews.
    """

    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    http_methods_names = [
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
        'trace'
    ]
    # permission_classes = ()

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs['title_id'])
        )
