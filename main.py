import aio_pika
import asyncio

async def main():
    connection = await aio_pika.connect("amqp://guest:guest@192.168.1.28")
    channel = await connection.channel()
    ex = channel.default_exchange
    q = await channel.declare_queue("user.create")
    async with q.iterator() as qi:
        message: aio_pika.abc.AbstractMessage
        async for message in qi:
            try:
                async with message.process(requeue=False):
                    assert message.reply_to is not None
                    n = message.body.decode()
                    response = "abc"
                    await ex.publish(
                        aio_pika.Message(
                            body=response.encode("utf-8"),
                            correlation_id=message.correlation_id
                        ),
                        routing_key=message.reply_to
                    )
            except Exception as e:
                print(e)

                print(message)


if __name__ == "__main__":
    asyncio.run(main())