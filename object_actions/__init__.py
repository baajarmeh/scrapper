"""A Django app for adding object tools for models in the admin."""

from .utils import (
    BaseDjangoObjectActions,
    DjangoObjectActions,
    takes_instance_or_queryset,
)
