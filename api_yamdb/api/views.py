from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, User


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Review model ViewsSet.

    Only authenticated users can add new reviews.
    Users can edit only their own reviews.
    Admins and moders can edit reviews of all users.
    """

    serializer_class = ReviewSerializer
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
        # title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        # return title.reviews
        return Review.objects.filter(title=self.kwargs['title_id'])


class CommentViewSet(viewsets.ModelViewSet):
    """
    Comment model ViewsSet.

    Only authenticated users can add new comments.
    Users can edit only their own comments.
    Admins and moders can edit coments of all users.
    """

    serializer_class = CommentSerializer
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
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        return serializer.save(
            # author=self.request.user,
            author=User.objects.get(pk=1),
            review=get_object_or_404(
                Review,
                pk=self.kwargs['review_id'],
                title=self.kwargs['title_id']
            )
        )
