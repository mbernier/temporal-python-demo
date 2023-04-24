import os

def function_one():
    return "one"

def function_two():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f = open(os.path.join(__location__, "some_text.txt"), "r+")
    content = f.read()
    
    if len(content) > 0:
        f.close()
        return "two"
    
    f.write("two")
    f.close()
    raise Exception("😈😈😈 I am broken")

def function_three(): 
    return "three"

def function_four():
    # reset the file for the next run
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f = open(os.path.join(__location__, "some_text.txt"), "w")
    f.close()
    return "four"

counter = 0
class MyWorkflow: 

    def run(self):
        # returns "one"
        output = function_one()

        # returns "two", counter
        # throws exception if counter <= 0, to simulate a failed process downstream
        new_output = function_two()
        output += " " + new_output

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