import asyncio

import nats


async def main():
    nc = await nats.connect(servers=["nats://localhost:4222"])

    count: int = 0
    while True:
        print(".", end="")
        await nc.publish("foo", f"Hello #{count} from NATS publisher".encode('ascii'))
        await asyncio.sleep(1)
        count += 1

    await nc.close()


if __name__ == '__main__':
    asyncio.run(main())
