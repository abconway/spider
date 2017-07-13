import time

import boto3


def create_nat_gateway(allocation_id, subnet_id):
    ec2_client = boto3.client('ec2')

    nat_gateway = ec2_client.create_nat_gateway(
        AllocationId=allocation_id,
        SubnetId=subnet_id
    )['NatGateway']

    nat_gateway_waiter = ec2_client.get_waiter('nat_gateway_available')
    nat_gateway_waiter.wait(NatGatewayIds=[nat_gateway['NatGatewayId']])

    return nat_gateway


def delete_nat_gateway(nat_gateway_id):
    ec2_client = boto3.client('ec2')

    return ec2_client.delete_nat_gateway(NatGatewayId=nat_gateway_id)


def wait_for_nat_gateway_to_delete(vpc_id, nat_gateway_id):
    ec2_client = boto3.client('ec2')

    while True:
        # Roll our own waiter since the nat_gateway_available waiter breaks with the 'deleted' state
        found_nat_gateways = ec2_client.describe_nat_gateways(
            Filters=[
                {'Name': 'vpc-id', 'Values': [vpc_id]},
                {'Name': 'nat-gateway-id', 'Values': [nat_gateway_id]},
                {'Name': 'state', 'Values': ['deleted']},
            ]
        )['NatGateways']
        if len(found_nat_gateways) > 0:
            break
        time.sleep(5)
