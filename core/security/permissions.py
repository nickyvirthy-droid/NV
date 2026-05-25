from core.security.errors import (
    PermissionDeniedError
)


class PermissionManager:

    def __init__(
        self,
        admin_mode: bool = False,
    ):

        self.admin_mode = admin_mode

    def validate(
        self,
        action_definition,
    ):

        if (
            action_definition.admin_only
            and
            not self.admin_mode
        ):

            raise PermissionDeniedError(
                "Admin mode required"
            )

        if (
            action_definition.dangerous
            and
            not self.admin_mode
        ):

            raise PermissionDeniedError(
                "Dangerous action blocked"
            )

        return True
