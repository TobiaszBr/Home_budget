from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ModelViewSetWithoutEditing(mixins.CreateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin,
                                 mixins.ListModelMixin,
                                 GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `destroy()`
    and `list()` actions.
    """
    pass
