#!/usr/bin/python3

# Windows:
# nats-server.exe -js REM Start NATS Server with JetStream
# nats account info REM Check JetStream status

# Linux:
# sudo nats-server -js # Start NATS Server with JetStream
# nats account info # Check JetStream status

import asyncio
import sys

# pip install nats-py
import nats
from nats.errors import NoServersError, TimeoutError


async def main():
    async def nats_error_handler(e):
        print(f"Error during connection attempt: {str(e)}")

    async def nats_disconnected_handler():
        print("NATS is disconnected")

    async def nats_reconnected_handler():
        print(f"NATS is reconnected to {nats_connector.connected_url.netloc}")

    async def nats_connection_closed_handler():
        print("NATS connection is closed")

    try:
        nats_connector = await nats.connect(servers=["nats://localhost:4222"],
                                            name="NATS JetStream example publisher",
                                            connect_timeout=10,
                                            ping_interval=20,  # Forcing a closed connection after 20 * 6 = 120 s of inactivity
                                            max_outstanding_pings=6,
                                            allow_reconnect=True,
                                            dont_randomize=False,
                                            reconnect_time_wait=5,
                                            no_echo=False,
                                            error_cb=nats_error_handler,
                                            disconnected_cb=nats_disconnected_handler,
                                            reconnected_cb=nats_reconnected_handler,
                                            closed_cb=nats_connection_closed_handler,
                                            token="123456781234567812345678")
    except BaseException as e:
        print(f"Unhandled error during connection attempt: {str(e)}")
        sys.exit(1)  # Exiting the program with non-zero exit code

    jstream = nats_connector.jetstream()
    sample_kv = await jstream.create_key_value(bucket="sample_kv")
    print("Run NATS publisher with key/value store")

    count: int = 0
    while True:
        print(".", end="")

        await sample_kv.put(key="key", value=f"Hello #{count} from Key/Value NATS publisher".encode("ascii"))

        await asyncio.sleep(1)
        count += 1

    try:
        await nats_connector.flush(timeout=5)
    except TimeoutError as e:
        print(f"Flush timeout: {str(e)}")

    await delete_key_value(bucket="sample_kv")
    await nats_connector.drain()


if __name__ == "__main__":
    asyncio.run(main())
