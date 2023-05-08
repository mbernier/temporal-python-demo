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
        retryPolicy = RetryPolicy(
            initial_interval=timedelta(minutes=2),
            backoff_coefficient=float(1.0),
            maximum_interval=timedelta(minutes=50),
            maximum_attempts=4
        )

        # result = await temporal_client.execute_workflow(
        #     MyWorkflow.run,
        #     id="my-workflow-2",
        #     task_queue="default"
        # )

        try:
            # logging.info('in try')
            print("in try")
            workflow_handle = await temporal_client.start_workflow(
                MyWorkflow.run,
                id="my-workflow-2",
                task_queue="default",
                retry_policy=retryPolicy
            )
        except exceptions.WorkflowAlreadyStartedError as err:
            print("workflow was already running, getting the handle")
            workflow_handle = temporal_client.get_workflow_handle_for(
                MyWorkflow.run,
                "my-workflow-2"
            )
        result = await workflow_handle.result()
        print(f"\n\nThe end response: \n\n{result}\n\n")

if __name__ == "__main__":
    asyncio.run(main())