import aio_pika
import json
import os

async def publish_message(queue_name: str, message: dict):
    """
    Publishes a message to a specified RabbitMQ queue.
    """
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost/')
    
    try:
        connection = await aio_pika.connect_robust(rabbitmq_url)
        
        async with connection:
            channel = await connection.channel()
            
            queue = await channel.declare_queue(
                queue_name,
                auto_delete=False,
                durable=True
            )
            
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode()
                ),
                routing_key=queue.name,
            )
            print(f"Published message to queue '{queue_name}': {message}")
            
    except Exception as e:
        print(f"Error publishing message to RabbitMQ: {e}")
