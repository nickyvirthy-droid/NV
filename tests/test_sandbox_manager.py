from pathlib import Path

from core.coder import (
    SandboxManager
)

sandbox = SandboxManager()

Path(
    "teste_sandbox.txt"
).write_text(
    "NV"
)

copy_file = sandbox.create_copy(
    "teste_sandbox.txt"
)

print(
    Path(copy_file).exists()
)

sandbox.remove_copy(
    copy_file
)

Path(
    "teste_sandbox.txt"
).unlink()
