import boto3


def create_elastic_ip():
    ec2_client = boto3.client('ec2')

    return ec2_client.allocate_address(Domain='vpc')


def delete_elastic_ip(allocation_id):
    ec2_client = boto3.client('ec2')

    return ec2_client.release_address(AllocationId=allocation_id)
