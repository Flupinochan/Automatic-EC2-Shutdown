import boto3

ec2_client = boto3.client("ec2")


def lambda_handler(event, context):
    try:
        action = event["action"]
        ec2_ids = ec2_describe(action)
        if ec2_ids:
            if action == "start":
                ec2_start(ec2_ids)
            elif action == "stop":
                ec2_stop(ec2_ids)
    except:
        print("lambda_handlerにて、エラーが発生しました")


def ec2_describe(action):
    try:
        if action == "start":
            ec2_status = "stopped"
        elif action == "stop":
            ec2_status = "running"
        ec2_ids = []
        paginator = ec2_client.get_paginator("describe_instances")
        response_iterator = paginator.paginate(
            Filters=[
                {
                    "Name": "instance-state-name",
                    "Values": [
                        ec2_status,
                    ],
                },
            ],
        )
        for response in response_iterator:
            for reservation in response["Reservations"]:
                for instance in reservation["Instances"]:
                    ec2_ids.append(instance["InstanceId"])
        return ec2_ids
    except:
        print("ec2_describeにて、エラーが発生しました")
        raise


def ec2_start(ec2_ids):
    try:
        ec2_client.start_instances(InstanceIds=ec2_ids)
    except:
        print("ec2_startにて、エラーが発生しました")
        raise


def ec2_stop(ec2_ids):
    try:
        ec2_client.stop_instances(InstanceIds=ec2_ids)
    except:
        print("ec2_stopにて、エラーが発生しました")
        raise
