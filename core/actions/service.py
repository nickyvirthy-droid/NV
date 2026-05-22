from core.actions.parser import (
    ActionParser,
)

from core.actions.path_resolver import (
    PathResolver,
)

class ActionService:
    def __init__(
        self,
        executor,
    ):
        self.executor = executor

    async def process_response(
        self,
        llm_response,
    ):
        parsed = (
            ActionParser.parse(
                llm_response
            )
        )

        if not parsed:
            return {
                "executed": False,
                "response": llm_response,
            }

        if "path" in parsed["payload"]:
            parsed["payload"]["path"] = (
                PathResolver.resolve(
                    parsed["payload"]["path"]
                )
            )

        result = (
            await self.executor.execute(
                parsed["action"],
                parsed["payload"],
            )
        )

        return {
            "executed": True,
            "action": parsed[
                "action"
            ],
            "result": result,
        }
