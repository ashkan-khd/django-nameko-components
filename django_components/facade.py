from abc import ABC


from nameko.rpc import rpc
from django_nameko import get_pool

from django_components.dependency import DjangoModels


class ComponentFacade(ABC):
    name: str
    models = DjangoModels()

    @rpc
    def ping(self, service_name):
        print(f"ping from {service_name}")
        return "pong"

    @classmethod
    def get_instance(cls):
        with get_pool().next() as pool:
            return getattr(pool, cls.name)
