# temporal-python-demo
Comparing coding with Temporal and not Temporal

This script looks at a remote file for a specific string. If it is not there, an exception is thrown. The old-way,.py will handle this with try...except and Temporal will handle this gracefully with a backoff and retry.


## orders.py
Will simulate getting an order event, looking to see if the customer ID exists in the database and holding the order until that customer ID does exist.
It is looking in the file where customer data is stored by customers.py, if it doesn't find the randomly generated email, it will retry until it does find it.

## customer.py
Writes the customer data to the data store, in this case a file. But it has a 3 second sleep, so that orders.py gets backed up waiting for the customer ID to show up.

## workflow.py
Connects to the workflows or creates them, simultes a script that accepts events from a webhook or other source. This same code could be inserted into an API endpoint if you wanted.

# To run this example
1. Start your [Temporal Server](https://github.com/temporalio/cli)
2. In one terminal window: `python worker.py` - starts the worker that hangs out waiting for tasks
3. In a second terminal window: `python workflow.py` - runs the workflow start code that makes everything happen

