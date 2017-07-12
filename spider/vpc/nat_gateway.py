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
