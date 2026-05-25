from core.runtime.registry import (
    RuntimeRegistry
)

from core.sessions.manager import (
    SessionManager
)

from llm.prompts.builder import (
    PromptBuilder
)


runtime = RuntimeRegistry()

sessions = SessionManager()

session = sessions.create(
    user_id="alex"
)

builder = PromptBuilder(
    runtime=runtime,
    session=session,
)

prompt = (
    builder.build_system_prompt()
)

print(prompt)
