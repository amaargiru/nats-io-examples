#!/usr/bin/python3

# Windows:
# nats-server.exe -js REM Start NATS with JetStream
# nats account info REM Check JetStream status

# Linux:
# sudo nats-server -js # Start NATS with JetStream
# nats account info # Check JetStream status

import asyncio

# pip install nats-py
import nats


async def main():
    async def nats_error_handler(e):
        print(f"Error during connection attempt: {str(e)}")

    async def nats_disconnected_handler():
        print("NATS is disconnected")

    async def nats_reconnected_handler():
        print(f"NATS is reconnected to {nats_connector.connected_url.netloc}")

    async def nats_connection_closed_handler():
        print("NATS connection is closed")

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
                                        no_echo=False,
                                        error_cb=nats_error_handler,
                                        disconnected_cb=nats_disconnected_handler,
                                        reconnected_cb=nats_reconnected_handler,
                                        closed_cb=nats_connection_closed_handler)
    sub = await nats_connector.subscribe("foo", cb=nats_receive_message_handler)
    print("Run NATS subscriber")

    while True:
        await asyncio.sleep(1)

    await nats_connector.close()


if __name__ == "__main__":
    asyncio.run(main())
