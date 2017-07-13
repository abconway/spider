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


def describe_subnet(subnet_id):
    ec2 = boto3.resource('ec2')

    subnet = ec2.Subnet(subnet_id)

    return {
        'subnet_id': subnet.subnet_id,
        'vpc_id': subnet.vpc_id,
        'assign_ipv6_address_on_creation': subnet.assign_ipv6_address_on_creation,
        'availability_zone': subnet.availability_zone,
        'available_ip_address_count': subnet.available_ip_address_count,
        'cidr_block': subnet.cidr_block,
        'default_for_az': subnet.default_for_az,
        'ipv6_cidr_block_association_set': subnet.ipv6_cidr_block_association_set,
        'map_public_ip_on_launch': subnet.map_public_ip_on_launch,
        'state': subnet.state,
        'tags': subnet.tags,
    }


def delete_subnet(subnet_id):
    ec2_client = boto3.client('ec2')

    return ec2_client.delete_subnet(SubnetId=subnet_id)
