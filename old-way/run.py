import time
from common.common import read_resource_old

def function_one():
    return read_resource_old("one")

def function_two():
    content = read_resource_old("two")

    print(f"content is {content}")

    if content != "two":
        raise Exception(f"\n\n😈😈😈 I am broken, because I expected 'two' in the content, but found '{content}' \n\n")

    return content

def function_three():
    return read_resource_old("three")

def function_four():
    return read_resource_old("four")

counter = 0
class MyWorkflow: 

    def run(self, try_again=False):
        # returns "one"
        output = function_one()

        # returns "two", counter
        # throws exception if counter <= 0, to simulate a failed process downstream
        try:
            output = " " + function_two()
        except Exception as err:
            if try_again:
                output = " " +function_two()
            else:
                raise err

        # returns "three"
        output += " " + function_three()

        # returns "four"
        output += " " + function_four()
        return output

if __name__ == "__main__":
    workflow = MyWorkflow()

    try:
        print("## Run the old way\n")
        print(workflow.run())
    except Exception as err:
        print("An exception occurred, this is the message received: ")
        print(err)
        
        print("\n\nWe are going to try to run this again...")
        time.sleep(3)
        print(workflow.run(True))