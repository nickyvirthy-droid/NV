from core.coder import CoderEngine

coder = CoderEngine()

result = coder.validator.run_tests()

print(
    result["success"]
)
