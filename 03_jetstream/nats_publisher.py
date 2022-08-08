import asyncio

import nats


async def main():
    nc = await nats.connect(servers=["nats://localhost:4222"])
    jstream = nc.jetstream()
    await jstream.add_stream(name="sample_stream", subjects=["foo"])
    print("Run NATS publisher with stream")

    count: int = 0
    while True:
        print(".", end="")

        ack = await jstream.publish("foo", f"Hello #{count} from NATS publisher".encode('ascii'))
        print(f"Ack: stream = \"{ack.stream}\", sequence = \"{ack.seq}\"")

        await asyncio.sleep(1)
        count += 1

    await nc.close()


if __name__ == '__main__':
    asyncio.run(main())
