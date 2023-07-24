# temporal-python-demo
Comparing coding with Temporal and not Temporal

This script looks at a remote file for a specific string. If it is not there, an exception is thrown. The old-way,.py will handle this with try...except and Temporal will handle this gracefully with a backoff and retry.

## old-way
This is a file that creates a string from concatenating the ouput of a series of functions when `python old-way.py` has been run.
You will see that the first run throws an exception, because the remote file does not have the expected data.
Then, on the second run, it will work because the file has been updated with the correct expected data.

## temporal
This shows how to add [Temporal python sdk](https://github.com/temporalio/sdk-python) to make the code durable.
It will run the same methods, and uses a "potentially" async file to control whether the exception is thrown.
Then, when the file gets updated, the code executes properly on a automatic retry from Temporal.

To run:
1. Start your [Temporal Server](https://github.com/temporalio/cli)
2. Run `python worker.py`

You will see that the first run throws an exception, because the remote file does not have the expected data.
Then, on the second run, it will work because the file has been updated with the correct expected data.

The difference is that Temporal will automatically retry to run your workflow, with a small incremental backoff.