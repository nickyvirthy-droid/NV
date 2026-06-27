from core.coder import (
    CodeAnalyzer
)

analyzer = CodeAnalyzer()

result = analyzer.analyze_file(
    "core/runtime/kernel.py"
)

print(
    result["file"]
)

print(
    result["lines"] > 0
)

print(
    isinstance(
        result["imports"],
        list
    )
)

print(
    isinstance(
        result["classes"],
        list
    )
)

print(
    isinstance(
        result["functions"],
        list
    )
)
