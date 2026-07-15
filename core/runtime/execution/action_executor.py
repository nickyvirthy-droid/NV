"""
OMEGA DRAKON • SYSTEMS

Action Executor
"""

from __future__ import annotations

import asyncio


class ActionExecutor:

    async def execute(
        self,
        *,
        step,
        payload,
        kernel,
    ):

        if step.timeout:

            return await asyncio.wait_for(
                kernel.actions.execute(
                    action_name=step.action_name,
                    payload=payload,
                ),
                timeout=step.timeout,
            )

        return await kernel.actions.execute(
            action_name=step.action_name,
            payload=payload,
        )
