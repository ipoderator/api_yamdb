from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Mixin for use Get, Create and Delete methods in Viewset."""

    lookup_field = 'slug'
    search_fields = ['name']
