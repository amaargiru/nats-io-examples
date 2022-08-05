import asyncio

import nats


async def main():
    nc = await nats.connect("nats://localhost:4222", user_credentials="user.creds")
    print("Run NATS publisher")

    count: int = 0
    while True:
        print(".", end="")
        await nc.publish("foo", f"Hello #{count} from NATS publisher".encode('ascii'))
        await asyncio.sleep(1)
        count += 1

    await nc.close()


if __name__ == '__main__':
    asyncio.run(main())
