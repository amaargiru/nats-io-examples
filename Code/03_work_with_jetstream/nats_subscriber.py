#!/usr/bin/python3

# Windows:
# nats-server.exe -js REM Start NATS Server with JetStream
# nats account info REM Check JetStream status

# Linux:
# sudo nats-server -js # Start NATS Server with JetStream
# nats account info # Check JetStream status

import asyncio

# pip install nats-py
import nats


async def main():
    async def nats_receive_message_handler(msg):
        print(f"Received a message from subject \"{msg.subject}\" (reply = \"{msg.reply}\"): {msg.data.decode()}")

    nats_connector = await nats.connect(servers=["nats://localhost:4222"],
                                        name="NATS JetStream example subscriber",
                                        connect_timeout=10,
                                        ping_interval=20,  # Forcing a closed connection after 20 * 6 = 120 s of inactivity
                                        max_outstanding_pings=6,
                                        allow_reconnect=True,
                                        dont_randomize=False,
                                        reconnect_time_wait=5,
                                        no_echo=False)
    sub = await nats_connector.subscribe("foo", cb=nats_receive_message_handler)
    print("Run NATS subscriber")

    while True:
        await asyncio.sleep(1)

    sub.unsubscribe()
    await nats_connector.drain()


if __name__ == "__main__":
    asyncio.run(main())
