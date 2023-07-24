import random, uuid, time, json
from common.common import read_resource
from datetime import timedelta
from temporalio import activity, workflow

sleep_time_seconds = 10

@activity.defn
async def create_order(order_data:dict):
    print(f"Creating Order with the following data: {order_data}")
    time.sleep(1)
    order_id = random.randint(1354, 9999)
    return order_id

@activity.defn
async def check_for_user(customer_email:str):
    print("Checking for the user")

    content = read_resource()

    if content == None:
        raise Exception(f"\n\n😈😈😈 No data in the remote datastore. \n\n")
    
    # get the data
    json_content = json.loads(content)

    # see if the email is in the data
    if customer_email not in json_content.keys():
        raise Exception(f"\n\n😈😈😈 Could not find a userID with the email '{customer_email}' in  the data store.\n\n")

    # return the customer_id
    return json_content[customer_email]

@activity.defn
async def fulfill_order(order_id): 
    print("The order fulfillment has been automatically sent to the warehouse")
    time.sleep(1)
    return uuid.uuid4()

@workflow.defn
class OrderWorkflow:

    @workflow.run
    async def run(self, order_data:dict):
        customer_id = await workflow.execute_activity(
            check_for_user,
            order_data['customer_email'],
            start_to_close_timeout=timedelta(seconds=3)
        )

        order_data['customer_id'] = customer_id
        
        order_id = await workflow.execute_activity(
            create_order,
            order_data,
            start_to_close_timeout=timedelta(seconds=5)
        )
        
        fulfillment_id = await workflow.execute_activity(
            fulfill_order,
            order_id,
            start_to_close_timeout=timedelta(seconds=3)
        )

        print(f"\n\nOrder Fulfilled: \n\n{order_data}\n\n")
        print("----------------------------------------------------------------")
        
        # hand fulfillment ID back to the workflow history
        return fulfillment_id