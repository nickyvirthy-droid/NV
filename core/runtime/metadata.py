from config.version import (
    ASSISTANT_NAME,
    SYSTEM_NAME,
    VERSION,
)


class RuntimeMetadata:
    @staticmethod
    def get():
        return {
            "system": SYSTEM_NAME,
            "assistant": ASSISTANT_NAME,
            "version": VERSION,
        }
