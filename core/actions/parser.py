import json


def parse_message(message: str):

    message = message.strip()

    if message.startswith("{"):

        return json.loads(message)

    lines = message.splitlines()

    result = {}

    for line in lines:

        if ":" not in line:
            continue

        key, value = line.split(
            ":",
            1
        )

        key = key.strip().upper()
        value = value.strip()

        if key == "ACTION":
            result["action"] = value

        elif key == "PATH":

            result["payload"] = {
                "path": value
            }

    return result
