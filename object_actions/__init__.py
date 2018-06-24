"""A Django app for adding object tools for models in the admin."""

from .utils import (
    BaseBaayObjectActions,
    BaayObjectActions,
    takes_instance_or_queryset,
)
