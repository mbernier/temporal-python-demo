import os
from datetime import timedelta
from temporalio import activity, workflow

@activity.defn
async def function_one():
    return "one"

@activity.defn
async def function_two():
    print("trying function two")
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f = open(os.path.join(__location__, "some_text.txt"), "r+")
    content = f.read()

    if len(content) > 0 :
        f.close()
        return content

    f.write("two")
    f.close()
    raise Exception("😈😈😈 I am broken\n\n")

@activity.defn
async def function_three(): 
    return "three"

@activity.defn
async def function_four():
    # reset the file
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f = open(os.path.join(__location__, "some_text.txt"), "w")
    f.close()
    # return what we need here
    return "four"

@workflow.defn
class MyWorkflow:

    @workflow.run
    async def run(self, var:str = None):
        output = await workflow.execute_activity(
            function_one,
            start_to_close_timeout=timedelta(seconds=3)
        )

        output += " " + await workflow.execute_activity(
            function_two,
            start_to_close_timeout=timedelta(seconds=3)
        )
        
        output += " " + await workflow.execute_activity(
            function_three,
            start_to_close_timeout=timedelta(seconds=3)
        )

        output += " " + await workflow.execute_activity(
            function_four,
            start_to_close_timeout=timedelta(seconds=3)
        )

        print(output)

