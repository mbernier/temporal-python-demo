from common.common import read_resource
from datetime import timedelta
from temporalio import activity, workflow

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

        return output