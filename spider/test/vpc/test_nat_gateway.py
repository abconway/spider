import unittest

import boto3
import moto

from spider.vpc import (
    create_vpc,
    create_elastic_ip,
    create_subnet,
    create_nat_gateway,
    delete_nat_gateway,
)


class TestNatGateway(unittest.TestCase):

    @moto.mock_ec2
    def test_create_nat_gateway(self):
        ec2_client = boto3.client('ec2')

        vpc = create_vpc(name='Test', cidr_block='10.0.0.0/16')
        subnet = create_subnet(name='TestSubnet', vpc_id=vpc.id, cidr_block='10.0.0.0/19', availability_zone='us-east-1a')
        elastic_ip = create_elastic_ip()

        nat_gateway = create_nat_gateway(
            allocation_id=elastic_ip['AllocationId'],
            subnet_id=subnet.id
        )

        nat_gateways = ec2_client.describe_nat_gateways(NatGatewayIds=[nat_gateway['NatGatewayId']])['NatGateways']
        found_nat_gateway = nat_gateways[0]

        self.assertEqual(nat_gateway['NatGatewayId'], found_nat_gateway['NatGatewayId'])
        self.assertIn(nat_gateway['SubnetId'], found_nat_gateway['SubnetId'])

    @moto.mock_ec2
    def test_delete_nat_gateway(self):
        ec2_client = boto3.client('ec2')

        vpc = create_vpc(name='Test', cidr_block='10.0.0.0/16')
        subnet = create_subnet(name='TestSubnet', vpc_id=vpc.id, cidr_block='10.0.0.0/19', availability_zone='us-east-1a')
        elastic_ip = create_elastic_ip()

        nat_gateway = create_nat_gateway(
            allocation_id=elastic_ip['AllocationId'],
            subnet_id=subnet.id
        )

        nat_gateways = ec2_client.describe_nat_gateways(NatGatewayIds=[nat_gateway['NatGatewayId']])['NatGateways']
        found_nat_gateway = nat_gateways[0]

        self.assertEqual(nat_gateway['NatGatewayId'], found_nat_gateway['NatGatewayId'])

        delete_nat_gateway(nat_gateway_id=nat_gateway['NatGatewayId'])

        nat_gateways = ec2_client.describe_nat_gateways(NatGatewayIds=[nat_gateway['NatGatewayId']])['NatGateways']
        nat_gateway_ids = [nat_gateway['NatGatewayId'] for nat_gateway in nat_gateways]

        self.assertNotIn(nat_gateway['NatGatewayId'], nat_gateway_ids)
