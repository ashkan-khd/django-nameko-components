import os

from django.conf import settings
from nameko.extensions import DependencyProvider


class DjangoModels(DependencyProvider):
    def ensure_django_settings(self):
        if not os.environ.get("DJANGO_SETTINGS_MODULE"):
            raise ModuleNotFoundError(
                "Could not connect to django models. "
                "You need to specify DJANGO_SETTINGS_MODULE in your PATH."
            )

    def setup(self):
        """
        Initialize the dependency
        """
        self.ensure_django_settings()

        import django

        django.setup()

    def get_dependency(self, worker_ctx):
        return type("NonExistingClass_", (), {})

    def worker_teardown(self, worker_ctx):
        """
        Close all the connections on teardown
        """
        from django.db import connections

        connections.close_all()
