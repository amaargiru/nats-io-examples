import asyncio

import nats


async def main():
    nats_connector = await nats.connect(servers=["nats://localhost:4222"],
                                        name="NATS simple example publisher",
                                        connect_timeout=10,
                                        ping_interval=20,  # Forcing a closed connection after 20 * 6 = 120 s of inactivity
                                        max_outstanding_pings=6,
                                        allow_reconnect=True,
                                        dont_randomize=False,
                                        reconnect_time_wait=5)
    print("Run NATS publisher")

    count: int = 0
    while True:
        print(".", end="")
        await nats_connector.publish("foo", f"Hello #{count} from NATS publisher".encode('ascii'))
        await asyncio.sleep(1)
        count += 1

    await nats_connector.close()


if __name__ == '__main__':
    asyncio.run(main())
