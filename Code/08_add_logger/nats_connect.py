import logging
import sys

import nats


class NatsConnect:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    async def connector(self):
        async def nats_error_handler(e):
            self.logger.error(f"Error during connection attempt: {str(e)}")

        async def nats_disconnected_handler():
            self.logger.error("NATS is disconnected")

        async def nats_reconnected_handler():
            self.logger.warning(f"NATS is reconnected")

        async def nats_connection_closed_handler():
            self.logger.error("NATS connection is closed")

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
        except Exception as e:
            self.logger.error(f"Unhandled error during connection attempt: {str(e)}")
            sys.exit(1)  # Exiting the program with non-zero exit code

        return nats_connector
