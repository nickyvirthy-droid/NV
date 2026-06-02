from dataclasses import dataclass


@dataclass
class PluginMetadata:

    name: str
    version: str
    author: str
    description: str
