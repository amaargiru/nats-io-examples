import asyncio

import nats


async def main():
    async def message_handler(msg):
        print(f"Received a message on \"{msg.subject} {msg.reply}\": {msg.data.decode()}")

    nc = await nats.connect(servers=["nats://localhost:4222"])
    sub = await nc.subscribe("foo", cb=message_handler)

    while True:
        await asyncio.sleep(1)

    await nc.close()


if __name__ == '__main__':
    asyncio.run(main())
