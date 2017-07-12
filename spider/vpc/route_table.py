import boto3


def create_route_table(name, vpc_id, subnet_id=None, routes=None, environment='development'):
    if not routes:
        routes = []

    ec2 = boto3.resource('ec2')

    route_table = ec2.create_route_table(VpcId=vpc_id)

    route_table.create_tags(
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

    for route in routes:
        route_table.create_route(**route)

    if subnet_id:
        route_table.associate_with_subnet(SubnetId=subnet_id)

    return route_table


def delete_route_table(route_table_id):
    ec2_client = boto3.client('ec2')

    return ec2_client.delete_route_table(RouteTableId=route_table_id)
