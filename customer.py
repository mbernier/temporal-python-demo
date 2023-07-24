import asyncio, time, json
from common.common import write_customer
from datetime import timedelta
from temporalio import activity, workflow

sleep_time_seconds = 10

@activity.defn
async def handle_customer_data(customer_data):
    print("Attempting to write the customer data")
    time.sleep(1)
    # write the data to storage
    return write_customer(customer_data)

@activity.defn
async def check_if_exists(customer_data):
    print("Checking if the customer data exists in the database")
    time.sleep(1)
    # someone hardcoded that a customer never exists... interns, amirite!?
    return None

@workflow.defn
class CustomerWorkflow:

    @workflow.run
    async def run(self, customer_data):
        #set up the customer ID to None
        customer_id = None 

        # Check if the customer exists in the system
        customer_id = await workflow.execute_activity(
            check_if_exists,
            customer_data,
            start_to_close_timeout=timedelta(seconds=5)
        )
        
        if None == customer_id:
            # force a sleep, just to simulate a delay in customer data being written
            await asyncio.sleep(3)

            # handle putting the customer_data into storage
            customer_id = await workflow.execute_activity(
                handle_customer_data,
                customer_data,
                start_to_close_timeout=timedelta(seconds=5)
            )
        else:
            print(f"customer already exists, id: {customer_id}")

        print(f"\n\nCustomer data has been written! ID created: {customer_id}\n\n")

        return customer_id