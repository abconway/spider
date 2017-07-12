import boto3
from botocore.exceptions import ClientError


def create_vpc(name, cidr_block, environment='development'):
    ec2 = boto3.resource('ec2')
    ec2_client = boto3.client('ec2')

    vpc = ec2.create_vpc(
        CidrBlock=cidr_block,
    )

    vpc_waiter = ec2_client.get_waiter('vpc_available')
    vpc_waiter.wait(VpcIds=[vpc.id])

    vpc.create_tags(
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

    return vpc


def delete_vpc(vpc_id, force=False, debug=False):
    ec2_client = boto3.client('ec2')

    try:
        return ec2_client.delete_vpc(VpcId=vpc_id)
    except ClientError as error:
        if 'DependencyViolation' in error.response['Error']['Code'] and not force:
            raise error

        ec2 = boto3.resource('ec2')
        vpc = ec2.Vpc(vpc_id)

        for route_table in vpc.route_tables.all():
            main = False
            for route_table_association in route_table.associations:
                if route_table_association.main:
                    main = True
                else:
                    route_table_association.delete()
            if not main:
                route_table.delete()

        nat_gateways = ec2_client.describe_nat_gateways(
            Filters=[
                {'Name': 'vpc-id', 'Values': [vpc_id]},
                {'Name': 'state', 'Values': ['available']},
            ]
        )['NatGateways']

        for nat_gateway in nat_gateways:
            ec2_client.delete_nat_gateway(NatGatewayId=nat_gateway['NatGatewayId'])

            if not debug:
                nat_gateway_waiter = ec2_client.get_waiter('nat_gateway_available')
                nat_gateway_waiter.wait(
                    Filters=[{'Name': 'state', 'Values': ['deleted']}],
                    NatGatewayIds=[nat_gateway['NatGatewayId']],
                )

            for nat_gateway_address in nat_gateway['NatGatewayAddresses']:
                ec2_client.release_address(AllocationId=nat_gateway_address['AllocationId'])

        for internet_gateway in vpc.internet_gateways.all():
            internet_gateway.detach_from_vpc(VpcId=vpc_id)
            internet_gateway.delete()

        for subnet in vpc.subnets.all():
            subnet.delete()

        ec2_client.delete_vpc(VpcId=vpc_id)