import unittest
from unittest.mock import patch

import boto3
import moto

from spider.vpc import (
    create_vpc,
    delete_vpc,
    create_subnet,
    create_elastic_ip,
    create_nat_gateway,
    create_internet_gateway,
    create_route_table,
)


class TestVpc(unittest.TestCase):

    @moto.mock_ec2
    def test_create_vpc(self):
        ec2_client = boto3.client('ec2')

        vpc = create_vpc(name='Test', cidr_block='10.0.0.0/16')

        vpcs = ec2_client.describe_vpcs(VpcIds=[vpc.id])['Vpcs']
        found_vpc = vpcs[0]

        self.assertEqual(vpc.id, found_vpc['VpcId'])
        self.assertEqual(vpc.cidr_block, '10.0.0.0/16')

    @moto.mock_ec2
    @patch('spider.vpc.vpc.wait_for_nat_gateway_to_delete')
    def test_delete_vpc(self, mock_wait_for_nat_gateway_to_delete):
        mock_wait_for_nat_gateway_to_delete.return_value = None

        ec2_client = boto3.client('ec2')

        vpc = create_vpc(name='Test', cidr_block='10.0.0.0/16')

        public_subnet = create_subnet(
            name='TestPublicSubnet',
            vpc_id=vpc.id,
            cidr_block='10.0.0.0/19',
            availability_zone='us-east-1a',
        )
        private_subnet = create_subnet(
            name='TestPrivateSubnet',
            vpc_id=vpc.id,
            cidr_block='10.0.128.0/19',
            availability_zone='us-east-1a',
        )

        internet_gateway = create_internet_gateway(name='TestGateway', vpc_id=vpc.id)

        elastic_ip = create_elastic_ip()

        nat_gateway = create_nat_gateway(
            allocation_id=elastic_ip['AllocationId'],
            subnet_id=private_subnet.id
        )

        public_route_table = create_route_table(
            name='TestRoutePublic',
            vpc_id=vpc.id,
            subnet_id=public_subnet.id,
            routes=[
                {
                    'DestinationCidrBlock': '0.0.0.0/0',
                    'GatewayId': internet_gateway.id,
                },
            ]
        )

        private_route_table = create_route_table(
            name='TestRoutePrivate',
            vpc_id=vpc.id,
            subnet_id=private_subnet.id,
            routes=[
                {
                    'DestinationCidrBlock': '0.0.0.0/0',
                    'NatGatewayId': nat_gateway['NatGatewayId'],
                },
            ]
        )

        vpcs = ec2_client.describe_vpcs(VpcIds=[vpc.id])['Vpcs']
        found_vpc = vpcs[0]

        self.assertIn(vpc.id, found_vpc['VpcId'])
        self.assertEqual(vpc.cidr_block, '10.0.0.0/16')

        delete_vpc(vpc_id=vpc.id, force=True)

        vpcs = ec2_client.describe_vpcs(VpcIds=[vpc.id])['Vpcs']

        self.assertEqual(len(vpcs), 0)
