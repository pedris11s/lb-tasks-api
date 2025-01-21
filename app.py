#!/usr/bin/env python3
import os

from aws_cdk import App

from lb_tasks_api.lb_tasks_api_stack import LbTasksApiStack


stage = os.getenv('STAGE', 'prod')
stack_name = f"lb-tasks-service-{stage}"

app = App()
LbTasksApiStack(app, stack_name)
app.synth()
