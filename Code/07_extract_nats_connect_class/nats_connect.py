import sys

import nats


class NatsConnect:
    async def connector(self):
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
                                                closed_cb=nats_connection_closed_handler)
        except BaseException as e:
            print(f"Unhandled error during connection attempt: {str(e)}")
            sys.exit(1)  # Exiting the program with non-zero exit code

        return nats_connector
