from core.events.event import Event


async def log_all_events(event: Event):
    print(
        f"[EVENT] {event.type} from {event.source}"
    )
