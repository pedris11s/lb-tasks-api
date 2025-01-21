from aws_cdk import Stack, RemovalPolicy, CfnOutput
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType, BillingMode
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.aws_apigateway import RestApi, LambdaIntegration
from constructs import Construct


class LbTasksApiStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        table = Table(
            self,
            "TasksTable",
            table_name=f"{id}-tasks",
            partition_key=Attribute(name="taskId", type=AttributeType.STRING),
            billing_mode=BillingMode.PAY_PER_REQUEST,  # Enables on-demand billing
            removal_policy=RemovalPolicy.DESTROY,  # Set to RETAIN for production
        )

        # Lambda Environment Variables
        lambda_env = {"TABLE_NAME": table.table_name}

        # Create Lambda Functions
        create_task_lambda = Function(
            self,
            "CreateTaskFunction",
            runtime=Runtime.PYTHON_3_9,
            handler="handler.create_task",  # Specify the method in handler.py
            code=Code.from_asset("src/lambdas"),  # Directory with handler and dependencies
            environment=lambda_env,
            function_name=f"{id}-create-task",
        )

        get_task_lambda = Function(
            self,
            "GetTaskFunction",
            runtime=Runtime.PYTHON_3_9,
            handler="handler.get_task",
            code=Code.from_asset("src/lambdas"),
            environment=lambda_env,
            function_name=f"{id}-get-task",
        )

        update_task_lambda = Function(
            self,
            "UpdateTaskFunction",
            runtime=Runtime.PYTHON_3_9,
            handler="handler.update_task",
            code=Code.from_asset("src/lambdas"),
            environment=lambda_env,
            function_name=f"{id}-update-task",
        )

        delete_task_lambda = Function(
            self,
            "DeleteTaskFunction",
            runtime=Runtime.PYTHON_3_9,
            handler="handler.delete_task",
            code=Code.from_asset("src/lambdas"),
            environment=lambda_env,
            function_name=f"{id}-delete-task",
        )

        # Grant Permissions to Lambdas
        table.grant_read_write_data(create_task_lambda)
        table.grant_read_data(get_task_lambda)
        table.grant_read_write_data(update_task_lambda)
        table.grant_write_data(delete_task_lambda)

        # API Gateway
        api = RestApi(
            self,
            "TasksApi",
            rest_api_name=f"{id}-api",
            description="API for managing tasks.",
        )

        # API Resources and Methods
        tasks = api.root.add_resource("tasks")
        task = tasks.add_resource("{taskId}")

        tasks.add_method("POST", LambdaIntegration(create_task_lambda))
        task.add_method("GET", LambdaIntegration(get_task_lambda))
        task.add_method("PUT", LambdaIntegration(update_task_lambda))
        task.add_method("DELETE", LambdaIntegration(delete_task_lambda))

        # Outputs
        CfnOutput(self, "ApiUrl", value=api.url)
