import boto3


def create_subnet(name, vpc_id, availability_zone, cidr_block, environment='development'):
    ec2 = boto3.resource('ec2')
    ec2_client = boto3.client('ec2')

    subnet = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock=cidr_block,
        AvailabilityZone=availability_zone,
    )

    subnet_waiter = ec2_client.get_waiter('subnet_available')
    subnet_waiter.wait(SubnetIds=[subnet.id])

    subnet.create_tags(
        Tags=[
            {
                'Key': 'Name',
                'Value': name,
            },
            {
                'Key': 'voxy:environment',
                'Value': environment,
            },
        ],
    )

    return subnet


def delete_subnet(subnet_id):
    ec2_client = boto3.client('ec2')

    return ec2_client.delete_subnet(SubnetId=subnet_id)
