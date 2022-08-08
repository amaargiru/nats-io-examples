import asyncio

import nats


async def main():
    nats_connector = await nats.connect("nats://localhost:4222", user_credentials="user.creds")
    print("Run NATS publisher with creds")

    count: int = 0
    while True:
        print(".", end="")
        await nats_connector.publish("foo", f"Hello #{count} from NATS publisher".encode('ascii'))
        await asyncio.sleep(1)
        count += 1

    await nats_connector.close()


if __name__ == '__main__':
    asyncio.run(main())
