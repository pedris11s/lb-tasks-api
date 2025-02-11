import aws_cdk as core
import aws_cdk.assertions as assertions

from lb_tasks_api.lb_tasks_api_stack import LbTasksApiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lb_tasks_api/lb_tasks_api_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LbTasksApiStack(app, "lb-tasks-api")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
