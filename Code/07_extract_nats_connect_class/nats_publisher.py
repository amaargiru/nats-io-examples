#!/usr/bin/python3

# pip install nats-py

# Windows:
# nats-server.exe -js REM Start NATS Server with JetStream
# nats account info REM Check JetStream status

# Linux:
# sudo nats-server -js # Start NATS Server with JetStream
# nats account info # Check JetStream status

import asyncio

from nats.errors import TimeoutError

from nats_connect import NatsConnect


async def main():
    nats_connect = NatsConnect()
    nats_connector = await nats_connect.connector()

    jstream = nats_connector.jetstream()
    await jstream.add_stream(name="sample_stream", subjects=["foo"])
    print("Run NATS publisher with stream")

    count: int = 0
    while True:
        ack = await jstream.publish("foo", f"Hello #{count} from NATS publisher".encode("ascii"))
        print(f"Ack: stream = \"{ack.stream}\", sequence = \"{ack.seq}\"")

        await asyncio.sleep(1)
        count += 1

    try:
        await nats_connector.flush(timeout=5)
    except TimeoutError as e:
        print(f"Flush timeout: {str(e)}")

    await nats_connector.drain()


if __name__ == "__main__":
    asyncio.run(main())
