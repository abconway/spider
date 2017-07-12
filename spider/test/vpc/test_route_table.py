import unittest

import boto3
import moto

from spider.vpc import (
    create_vpc,
    create_route_table,
    delete_route_table,
    create_subnet,
    create_internet_gateway,
)


class TestRouteTable(unittest.TestCase):
    @moto.mock_ec2
    def test_create_route_table(self):
        ec2_client = boto3.client('ec2')

        vpc = create_vpc(name='Test', cidr_block='10.0.0.0/16')

        route_table = create_route_table(
            name='TestRouteTable',
            vpc_id=vpc.id,
        )

        route_tables = ec2_client.describe_route_tables(RouteTableIds=[route_table.id])['RouteTables']
        found_route_table = route_tables[0]

        self.assertEqual(route_table.id, found_route_table['RouteTableId'])
        self.assertEqual(route_table.vpc_id, found_route_table['VpcId'])

    @moto.mock_ec2
    def test_delete_route_table(self):
        ec2_client = boto3.client('ec2')

        vpc = create_vpc(name='Test', cidr_block='10.0.0.0/16')

        route_table = create_route_table(
            name='TestRouteTable',
            vpc_id=vpc.id,
        )

        route_tables = ec2_client.describe_route_tables(RouteTableIds=[route_table.id])['RouteTables']
        found_route_table = route_tables[0]

        self.assertEqual(route_table.id, found_route_table['RouteTableId'])

        delete_route_table(route_table_id=route_table.id)

        route_tables = ec2_client.describe_route_tables()['RouteTables']
        route_table_ids = [table['RouteTableId'] for table in route_tables]

        self.assertNotIn(route_table.id, route_table_ids)

    @moto.mock_ec2
    def test_routes(self):
        ec2_client = boto3.client('ec2')

        vpc = create_vpc(name='Test', cidr_block='10.0.0.0/16')
        subnet = create_subnet(name='TestSubnet', vpc_id=vpc.id, cidr_block='10.0.0.0/19',
                               availability_zone='us-east-1a')
        internet_gateway = create_internet_gateway(name='TestGateway', vpc_id=vpc.id)

        route_table = create_route_table(
            name='TestRoutePublic',
            vpc_id=vpc.id,
            subnet_id=subnet.id,
            routes=[
                {
                    'DestinationCidrBlock': '0.0.0.0/0',
                    'GatewayId': internet_gateway.id,
                },
            ]
        )

        found_route_tables = ec2_client.describe_route_tables(RouteTableIds=[route_table.id])['RouteTables']

        found_routes = []
        for table in found_route_tables:
            for route in table['Routes']:
                found_routes.append(route)
        found_gateway_ids = [route.get('GatewayId') for route in found_routes]

        self.assertIn(internet_gateway.id, found_gateway_ids)
