from core.actions.parser import (
    parse_message,
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

        parsed = parse_message(
            llm_response
        )

        if not parsed:

            return {
                "executed": False,
                "response": llm_response,
            }

        payload = parsed.get(
            "payload",
            {}
        )

        if "path" in payload:

            payload["path"] = (
                PathResolver.resolve(
                    payload["path"]
                )
            )

        result = (
            await self.executor.execute(
                parsed["action"],
                payload,
            )
        )

        return {
            "executed": True,
            "action": parsed[
                "action"
            ],
            "result": result,
        }
