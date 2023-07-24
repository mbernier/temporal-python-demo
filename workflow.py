import asyncio, random
from datetime import timedelta
from orders import OrderWorkflow
from customer import CustomerWorkflow
from temporalio import service, exceptions
from temporalio.worker import Worker
from temporalio.client import Client


async def run_workflows(customer_data, order_data):
    temporal_client = await Client.connect("localhost:7233", namespace="default")

    try:
        # add the user to the database if they don't exist
        customer_workflow_handle = await temporal_client.start_workflow(
            CustomerWorkflow.run,
            customer_data,
            id="customer_workflow",
            task_queue="default"
        )

        # pass the customer email on the order
        order_data['customer_email'] = customer_data['email']

        # perform the order
        order_workflow_handle = await temporal_client.start_workflow(
            OrderWorkflow.run,
            order_data,
            id="order_workflow",
            task_queue="default"
        )
    except exceptions.WorkflowAlreadyStartedError as err:
        
        print("\n\n\nCONNECTING TO OLD ACTIVE WORKFLOWS\n\n\n")
        
        customer_workflow_handle = temporal_client.get_workflow_handle_for(
            CustomerWorkflow.run,
            "customer_workflow"
        )

        order_workflow_handle = temporal_client.get_workflow_handle_for(
            OrderWorkflow.run,
            "order_workflow"
        )

    customer_result = await customer_workflow_handle.result()
    order_result = await order_workflow_handle.result()

    print(f"\n\nCustomer Workflow response: \n\n{customer_result}\n\n")
    print(f"\n\nOrder Workflow response: \n\n{order_result}\n\n")
    print("----------------------------------------------------------------")

if __name__ == "__main__":

    customer_data = {
        "name": "",
        "email": f"example{random.randint(1000,9999)}@example.com",
        "phone": "+11234567890",
        "street": "1234 Sesame Street",
        "city": "Sesame Street Village",
        "state": "California"
    }

    order_data = {
        "items": [
            {
                "SKU": "ASFHS&SDGSO",
                "count": 3,
                "price": 3.25
            },
            {
                "SKU": "G_1234SFH_762d",
                "count": 2,
                "price": 700.82
            }
        ],
        "total": 1411.39
    }

    asyncio.run(run_workflows(customer_data, order_data))