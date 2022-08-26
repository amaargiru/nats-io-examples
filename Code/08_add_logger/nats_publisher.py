#!/usr/bin/python3

# pip install nats-py

# Windows:
# nats-server.exe -js REM Start NATS Server with JetStream
# nats account info REM Check JetStream status

# Linux:
# sudo nats-server -js # Start NATS Server with JetStream
# nats account info # Check JetStream status

import asyncio
import os
import pathlib
import sys

from nats.errors import TimeoutError

from logger import NatsLogger
from nats_connect import NatsConnect

log_file_path: str = "logs/nats_publisher.log"  # Path to logs
log_max_file_size: int = 1024 ** 2  # Max log file size
log_max_file_count: int = 10  # Max number of log files


async def main():
    nats_connect = NatsConnect(logger)
    nats_connector = await nats_connect.connector()

    jstream = nats_connector.jetstream()
    await jstream.add_stream(name="sample_stream", subjects=["foo"])
    logger.info("Run NATS publisher with stream")

    count: int = 0
    while True:
        ack = await jstream.publish("foo", f"Hello #{count} from NATS publisher".encode("ascii"))
        logger.debug(f"Ack: stream = \"{ack.stream}\", sequence = \"{ack.seq}\"")

        await asyncio.sleep(1)
        count += 1

    try:
        await nats_connector.flush(timeout=5)
    except TimeoutError as e:
        logger.error(f"Flush timeout error: {str(e)}")

    await nats_connector.drain()


if __name__ == "__main__":
    try:
        path = pathlib.Path(log_file_path)  # Create a path to the log file(s) if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        logger = NatsLogger.get_logger(log_file_path, log_max_file_size, log_max_file_count)
    except Exception as err:
        print(f"Error when trying to create log directory: \"{str(err)}\"")
        sys.exit(1)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(" Exit from program by Ctrl-C")
        os._exit(1)
    except Exception as e:
        print(f"Error: {e}")
