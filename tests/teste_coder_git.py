from core.coder import CoderEngine

coder = CoderEngine()

print(
    coder.git.current_branch()
)

print(
    coder.git.status()
)
