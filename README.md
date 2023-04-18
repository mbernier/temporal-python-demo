# temporal-python-demo
Comparing coding with Temporal and not Temporal

## old-way
This is a file that creates a string from concatenating the ouput of a series of functions when `python old-way/run.py` has been run.
This will throw an exception every time, until you put in a try...except statement

## temporal
This shows how to add [Temporal python sdk](https://github.com/temporalio/sdk-python) to make the code durable.
It will run the same methods, and uses a "potentially" async file to control whether the exception is thrown.
Then, when the file gets updated, the code executes properly on a automatic retry from Temporal.