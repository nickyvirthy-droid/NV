class ActionParser:
    @staticmethod
    def parse(text):
        lines = text.splitlines()

        action = None
        payload = {}

        for line in lines:
            line = line.strip()

            if line.startswith(
                "ACTION:"
            ):
                action = (
                    line.replace(
                        "ACTION:",
                        "",
                    )
                    .strip()
                )

            if line.startswith(
                "PATH:"
            ):
                payload["path"] = (
                    line.replace(
                        "PATH:",
                        "",
                    )
                    .strip()
                )

        if not action:
            return None

        return {
            "action": action,
            "payload": payload,
        }
