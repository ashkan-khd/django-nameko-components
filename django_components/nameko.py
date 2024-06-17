import os

from django.conf import settings
from nameko.extensions import DependencyProvider


class DjangoModels(DependencyProvider):
    def get_settings_path(self) -> str:
        return "{}.settings".format(settings.ROOT_URLCONF.split(".")[0])

    def setup(self):
        """
        Initialize the dependency
        """
        import django

        if not os.environ.get("DJANGO_SETTINGS_MODULE"):
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", self.get_settings_path())
        django.setup()

    def get_dependency(self, worker_ctx):
        return type("NonExistingClass_", (), {})

    def worker_teardown(self, worker_ctx):
        """
        Close all the connections on teardown
        """
        from django.db import connections

        connections.close_all()
