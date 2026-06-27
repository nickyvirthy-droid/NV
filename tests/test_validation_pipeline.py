from core.coder import (
    ValidationEngine,
    ValidationPipeline
)

validator = (
    ValidationEngine()
)

pipeline = (
    ValidationPipeline(
        validator
    )
)

result = (
    pipeline.syntax_check(
        "core/runtime/kernel.py"
    )
)

print(result)
