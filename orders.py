import math, uuid
from common.common import read_resource
from datetime import timedelta
from temporalio import activity, workflow

sleep_time_seconds = 10

@activity.defn
async def create_order(order_data:dict):
    print(f"Creating Order with the following data: {order_data}")
    order_id = math.rand(1354, 9999)
    return order_id

@activity.defn
async def check_for_user(customer_email:str):
    print("Checking for the user")
    content = read_resource()
    return content

@activity.defn
async def fulfill_order(): 
    print("The order fulfillment has been automatically sent to the warehouse")
    return uuid.uuid()

@workflow.defn
class OrderWorkflow:

    @workflow.run
    async def run(self, order_data:dict, customer_email:str):
        customer_id = await workflow.execute_activity(
            check_for_user,
            customer_email,
            start_to_close_timeout=timedelta(seconds=20)
        )

        order_data['customer_id'] = customer_id
        
        order_id = await workflow.execute_activity(
            create_order,
            order_data,
            start_to_close_timeout=timedelta(seconds=30)
        )
        
        fulfillment_id = await workflow.execute_activity(
            fulfill_order,
            order_id,
            start_to_close_timeout=timedelta(seconds=30)
        )

        print(f"\n\nOrder Fulfilled: \n\n{order_data}\n\n")
        
        # hand fulfillment ID back to the workflow history
        return fulfillment_id