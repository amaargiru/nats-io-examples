#!/usr/bin/python3

# Windows:
# nats-server.exe -js REM Start NATS Server with JetStream
# nats account info REM Check JetStream status

# Linux:
# sudo nats-server -js # Start NATS Server with JetStream
# nats account info # Check JetStream status

import asyncio
import os

# pip install nats-py
import nats


async def main():
    nats_connector = await nats.connect(servers=["nats://localhost:4222"],
                                        name="NATS JetStream example publisher",
                                        connect_timeout=10,
                                        ping_interval=20,  # Forcing a closed connection after 20 * 6 = 120 s of inactivity
                                        max_outstanding_pings=6,
                                        allow_reconnect=True,
                                        dont_randomize=False,
                                        reconnect_time_wait=5,
                                        no_echo=False)
    jstream = nats_connector.jetstream()
    await jstream.add_stream(name="sample_stream", subjects=["foo"])
    print("Run NATS publisher with stream")

    count: int = 0
    while True:
        ack = await jstream.publish("foo", f"Hello #{count} from NATS publisher".encode("ascii"))
        print(f"Ack: stream = \"{ack.stream}\", sequence = \"{ack.seq}\"")

        await asyncio.sleep(1)
        count += 1

    await nats_connector.drain()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit from program by Ctrl-C")
        os._exit(1)
    except Exception as e:
        print(f"Error: {e}")
