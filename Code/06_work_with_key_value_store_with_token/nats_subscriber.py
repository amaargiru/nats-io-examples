#!/usr/bin/python3

# Windows:
# nats-server.exe -js REM Start NATS Server with JetStream
# nats account info REM Check JetStream status

# Linux:
# sudo nats-server -js # Start NATS Server with JetStream
# nats account info # Check JetStream status

import asyncio
import os
import sys

# pip install nats-py
import nats
from nats.errors import NoServersError, TimeoutError
from nats.js.errors import NotFoundError


async def main():
    async def nats_error_handler(e):
        print(f"Error during connection attempt: {str(e)}")

    async def nats_disconnected_handler():
        print("NATS is disconnected")

    async def nats_reconnected_handler():
        print(f"NATS is reconnected")

    async def nats_connection_closed_handler():
        print("NATS connection is closed")

    try:
        nats_connector = await nats.connect(servers=["nats://localhost:4222"],
                                            name="NATS JetStream example subscriber",
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

    print("Run NATS subscriber with key/value store")

    while True:
        try:
            entry = await sample_kv.get("key")
            print(f'KeyValue.Entry: key={entry.key}, value={entry.value}')
        except NotFoundError as e:
            print(str(e))
        finally:
            await asyncio.sleep(1)

    try:
        await nats_connector.flush(timeout=5)
    except TimeoutError as e:
        print(f"Flush timeout: {str(e)}")

    await nats_connector.drain()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit from program by Ctrl-C")
        os._exit(1)
    except Exception as e:
        print(f"Error: {e}")
