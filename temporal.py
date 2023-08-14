from common.common import read_resource
from datetime import timedelta
from temporalio import activity, workflow
import asyncio
from temporalio import service, exceptions
from temporalio.client import Client
from temporalio.common import RetryPolicy

sleep_time_seconds = 10

@activity.defn
async def function_one():
    return read_resource("one")

@activity.defn
async def function_two():
    content = read_resource("two")

    if content != "two":
        raise Exception(f"\n\n😈😈😈 I am broken, because I expected 'two' in the content, but found '{content}' \n\n")

    return content

@activity.defn
async def function_three(): 
    return read_resource("three")

@activity.defn
async def function_four():
    # return what we need here
    return read_resource("four")

@workflow.defn
class MyWorkflow:

    @workflow.run
    async def run(self, var:str = None):
        output = await workflow.execute_activity(
            function_one,
            start_to_close_timeout=timedelta(seconds=30)
        )

        output += " " + await workflow.execute_activity(
            function_two,
            start_to_close_timeout=timedelta(seconds=20)
        )
        
        output += " " + await workflow.execute_activity(
            function_three,
            start_to_close_timeout=timedelta(seconds=30)
        )

        output += " " + await workflow.execute_activity(
            function_four,
            start_to_close_timeout=timedelta(seconds=30)
        )

        print(f"\n\nThe end response: \n\n{output}\n\n")
        return output


async def run_workflow():
    temporal_client = await Client.connect("localhost:7233", namespace="default")
    
    retryPolicy = RetryPolicy(
        initial_interval=timedelta(minutes=2),
        backoff_coefficient=float(1.0),
        maximum_interval=timedelta(minutes=50),
        maximum_attempts=4
    )

    try:
        print("\n\nAttempting to create a new Workflow...")
        workflow_handle = await temporal_client.start_workflow(
            MyWorkflow.run,
            id="my-workflow-2",
            task_queue="default",
            retry_policy=retryPolicy
        )
    except exceptions.WorkflowAlreadyStartedError as err:
        print("Workflow was already running, getting the handle...")
        workflow_handle = temporal_client.get_workflow_handle_for(
            MyWorkflow.run,
            "my-workflow-2"
        )
    
    print("Running the workflow")
    result = await workflow_handle.result()
    print("Workflow complete\n\n")

if __name__ == "__main__":
    asyncio.run(run_workflow())