import logging
from typing import Optional
from models.task import Task
from botocore.exceptions import ClientError
import boto3
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskRepository:
    def __init__(self):
        self.table_name = os.environ.get("TABLE_NAME")
        if not self.table_name:
            raise ValueError("TABLE_NAME environment variable is not set.")
        self.dynamo_resource = boto3.resource("dynamodb")
        self.table = self.dynamo_resource.Table(self.table_name)

    def create_task(self, task: Task) -> None:
        try:
            logger.info(f"Creating task with ID {task.taskId} in table {self.table_name}")
            self.table.put_item(Item=task.dict())
            logger.info(f"Task with ID {task.taskId} created successfully.")
        except ClientError as e:
            logger.error(f"Error creating task {task.taskId}: {e}")
            raise Exception(f"Failed to create task {task.taskId}") from e

    def update_task(self, task_id: str, task: Task) -> None:
        try:
            logger.info(f"Updating task with ID {task_id} in table {self.table_name}")
            update_expression = []
            expression_attribute_values = {}

            for key, value in task.dict(exclude_none=True).items():
                if key != "taskId":
                    update_expression.append(f"{key} = :{key}")
                    expression_attribute_values[f":{key}"] = value

            if not update_expression:
                logger.warning(f"No attributes to update for task {task_id}")
                return

            self.table.update_item(
                Key={"taskId": task_id},
                UpdateExpression="SET " + ", ".join(update_expression),
                ExpressionAttributeValues=expression_attribute_values,
            )

            logger.info(f"Task with ID {task_id} updated successfully.")
        except ClientError as e:
            logger.error(f"Error updating task {task_id}: {e}")
            raise Exception(f"Failed to update task {task_id}") from e

    def get_task(self, task_id: str) -> Optional[Task]:
        try:
            logger.info(f"Retrieving task with ID {task_id} from table {self.table_name}")
            response = self.table.get_item(Key={"taskId": task_id})
            item = response.get("Item")
            if item:
                task = Task(**item)
                logger.info(f"Task with ID {task_id} retrieved successfully.")
                return task
            logger.warning(f"Task with ID {task_id} not found.")
            return None
        except ClientError as e:
            logger.error(f"Error retrieving task {task_id}: {e}")
            raise Exception(f"Failed to retrieve task {task_id}") from e

    def delete_task(self, task_id: str) -> None:
        try:
            logger.info(f"Deleting task with ID {task_id} from table {self.table_name}")
            self.table.delete_item(Key={"taskId": task_id})
            logger.info(f"Task with ID {task_id} deleted successfully.")
        except ClientError as e:
            logger.error(f"Error deleting task {task_id}: {e}")
            raise Exception(f"Failed to delete task {task_id}") from e
