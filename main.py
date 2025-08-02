import asyncio
import os
from app.grpc_server import serve
from app.messaging.consumer import start_consumer

async def main():
    """
    Main function to start both the gRPC server and the RabbitMQ consumer.
    """
    print("Starting gRPC server and RabbitMQ consumer...")
    await asyncio.gather(
        serve(),
        start_consumer()
    )

if __name__ == '__main__':
    os.environ['RABBITMQ_URL'] = 'amqp://guest:guest@localhost/'
    asyncio.run(main())

import asyncio

from app.grpc_server import serve

if __name__ == '__main__':
    asyncio.run(serve())

