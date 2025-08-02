import aio_pika
import asyncio
import json
import os
from uuid import UUID

from app.services.js_file_service import JSFileService

async def process_message(message: aio_pika.IncomingMessage):
    """
    Callback function to process incoming messages from the queue.
    """
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            print(f"Received message: {data}")

            files_to_add = []
            for file_data in data.get('files', []):
                # Basic validation for the required fields.
                if 'url' in file_data and 'priority' in file_data and 'company_id' in file_data:
                    files_to_add.append({
                        "url": file_data['url'],
                        "priority": file_data['priority'],
                        "company_id": UUID(file_data['company_id'])
                    })

            if files_to_add:
                service = JSFileService()
                await service.add_files(files_to_add)
                print(f"Successfully added {len(files_to_add)} files from queue.")

        except json.JSONDecodeError:
            print("Error: Message body is not valid JSON.")
        except Exception as e:
            print(f"Error processing message: {e}")

async def start_consumer():
    """
    Connects to RabbitMQ and starts consuming messages from the queue.
    """
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost/')

    try:
        connection = await aio_pika.connect_robust(rabbitmq_url)
        print("Connected to RabbitMQ.")

        async with connection:
            channel = await connection.channel()
            
            queue_name = "new_js_files"
            queue = await channel.declare_queue(
                queue_name,
                auto_delete=False,
                durable=True
            )

            print(f"Starting consumer for queue '{queue_name}'...")
            await queue.consume(process_message)
            
            await asyncio.Future()
            
    except aio_pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ: {e}")
    except Exception as e:
        print(f"An unexpected error occurred in the consumer: {e}")
