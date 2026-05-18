class RuntimeRegistry:
    def __init__(self):
        self._services: dict[str, object] = {}

    def register(self, name: str, service: object):
        self._services[name] = service

    def get(self, name: str):
        return self._services.get(name)

    def all(self):
        return self._services
