
def function_one():
    return "one"

def function_two(counter:int):
    if counter > 0:
        counter += 1
        return ("two", counter)
    raise Exception("😈😈😈 I am broken")

def function_three(): 
    return "three"

def function_four():
    return "four"

counter = 0

def run(counter:int):
    # returns "one"
    output = function_one()

    # returns "two", counter
    # throws exception if counter <= 0, to simulate a failed process downstream
    new_output, counter = function_two(counter)
    output += " " + new_output

    # returns "three"
    output += " " + function_three()

    # returns "four"
    output += " " + function_four()
    return output

if __name__ == "__main__":
    # counter += 1
    print("\n## Run 1\n")
    print(run(counter))
    print("\n")
    print("## Run 2")
    print(run(counter))