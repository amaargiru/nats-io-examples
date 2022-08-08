import asyncio

import nats


async def main():
    async def message_handler(msg):
        print(f"Received a message from subject \"{msg.subject}\" (reply = \"{msg.reply}\"): {msg.data.decode()}")

    nats_connector = await nats.connect(servers=["nats://localhost:4222"],
                                        name="NATS creds example subscriber",
                                        connect_timeout=10,
                                        ping_interval=20,  # Forcing a closed connection after 20 * 6 = 120 s of inactivity
                                        max_outstanding_pings=6,
                                        allow_reconnect=True,
                                        dont_randomize=False,
                                        reconnect_time_wait=5,
                                        user_credentials="user.creds")

    sub = await nats_connector.subscribe("foo", cb=message_handler)
    print("Run NATS subscriber with creds")

    while True:
        await asyncio.sleep(1)

    await nats_connector.close()


if __name__ == '__main__':
    asyncio.run(main())
