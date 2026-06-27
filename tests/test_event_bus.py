import asyncio

from core.events.bus import EventBus

bus = EventBus()

resultado = []


async def callback(payload):

    resultado.append(payload)


async def main():

    bus.subscribe(
        "teste",
        callback
    )

    await bus.emit(
        "teste",
        {
            "ok": True
        }
    )

    print(resultado)


asyncio.run(main())
