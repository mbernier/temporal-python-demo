import asyncio
from datetime import timedelta
from temporal import MyWorkflow, function_one, function_two, function_three, function_four
from temporalio import service, exceptions
from temporalio.worker import Worker
from temporalio.client import Client
from temporalio.common import RetryPolicy

interrupt_event = asyncio.Event()

async def main():
    # Connect client
    temporal_client = await Client.connect("localhost:7233", namespace="default")

    # Run a worker for the workflow
    async with Worker(
        temporal_client,
        task_queue="default",
        workflows=[MyWorkflow],
        activities=[function_one, function_two, function_three, function_four], #, do_client_handshake turned off for now
        graceful_shutdown_timeout=timedelta(seconds=0.5)
    ):

        await interrupt_event.wait()

if __name__ == "__main__":
    asyncio.run(main())