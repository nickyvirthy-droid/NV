"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Plugin Loader

Descrição: Descoberta e carregamento de plugins do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from pathlib import Path


IGNORED_DIRECTORIES = {
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
}


class PluginLoader:

    def __init__(self, plugin_dir="plugins"):

        self.plugin_dir = Path(plugin_dir)

    def discover(self):

        plugins = []

        if not self.plugin_dir.exists():
            return plugins

        for path in self.plugin_dir.iterdir():

            if not path.is_dir():
                continue

            if path.name.startswith("_"):
                continue

            if path.name in IGNORED_DIRECTORIES:
                continue

            plugins.append(path.name)

        return sorted(plugins)
