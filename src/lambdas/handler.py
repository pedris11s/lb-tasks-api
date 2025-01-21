import json
from repositories.task_repository import TaskRepository
from models.task import Task
from pydantic import ValidationError
from botocore.exceptions import ClientError

task_repo = TaskRepository()

def create_task(event, context):
    try:
        body = json.loads(event["body"])
        task = Task(**body)
        task_repo.create_task(task)
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Task created successfully"}),
        }
    except ValidationError as e:
        return {"statusCode": 400, "body": json.dumps({"error": "Validation error", "details": e.errors()})}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"error": "DynamoDB error", "details": str(e)})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error", "details": str(e)})}

def get_task(event, context):
    try:
        task_id = event["pathParameters"]["taskId"]
        task = task_repo.get_task(task_id)
        if task:
            return {"statusCode": 200, "body": task.json()}
        return {"statusCode": 404, "body": json.dumps({"error": "Task not found"})}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"error": "DynamoDB error", "details": str(e)})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error", "details": str(e)})}

def delete_task(event, context):
    try:
        task_id = event["pathParameters"]["taskId"]
        task_repo.delete_task(task_id)
        return {"statusCode": 200, "body": json.dumps({"message": "Task deleted"})}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"error": "DynamoDB error", "details": str(e)})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error", "details": str(e)})}

def update_task(event, context):
    try:
        task_id = event["pathParameters"]["taskId"]
        body = json.loads(event["body"])
        task = Task(**body)
        task_repo.update_task(task_id, task)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Task updated successfully"}),
        }
    except ValidationError as e:
        return {"statusCode": 400, "body": json.dumps({"error": "Validation error", "details": e.errors()})}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"error": "DynamoDB error", "details": str(e)})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error", "details": str(e)})}
