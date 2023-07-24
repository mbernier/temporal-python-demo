import os, time, uuid, json

sleep_time_seconds = 10

def read_resource_old(value=None, old=False):
    return read_resource(value, True)

def read_resource(value=None, old=False):
    file_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    if value == "four" or value == "one": # reset the file for the next run
        write_file(file_location, "one")
    elif value == "two": # read the file before writing the value, so it fails the first time
        value = read_file(file_location) # read what is there, it should be "one"
        write_file(file_location, "two")
        if value == "two":
            if old == True:
                print(f"""\nI am sleeping for {sleep_time_seconds} seconds, so the person demoing can talk 
about how the old-way/run.py file has a `try...except` and how this is necessary in the code to handle errors. 
Wouldn't your job (and your code) be so much simpler if this wasn't necessary?\n""")
            else:
                print(f"I am sleeping for {sleep_time_seconds} seconds, so the person demoing can show off the UI. Cmd+click here: http://127.0.0.1:8233\n")
            print_sleep(sleep_time_seconds) #output the fancy sleep time thing
    elif value != None:
        # Don't write the file if the data is none
        write_file(file_location, value)
    else:
        value = read_file(file_location)

    return value

def write_customer(customer_data):
    # create the customer ID for demo purposes here
    data = {
        customer_data['email']: str(uuid.uuid4())
    }

    # write the data to the storage
    read_resource(value=json.dumps(data))

    # return the customer_id
    return data[customer_data['email']]

def check_resource():
    read_resource("two")

def read_file(file_location):
    f = open(os.path.join(file_location, "some_text.txt"), "r")
    value = f.read()
    f.close()
    return value

def write_file(file_location, value:str):
    f = open(os.path.join(file_location, "some_text.txt"), "w")
    f.write(value)
    f.close()

def print_sleep(sleep_time_seconds):
    for x in reversed(range(sleep_time_seconds)):
        print(f"..{x}...", end = '\r')    
        time.sleep(1)
        if x == 0:
            print(" ", end = '\r')
