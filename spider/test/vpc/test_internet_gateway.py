import unittest

import boto3
import moto

from spider.vpc import (
    create_vpc,
    create_internet_gateway,
    delete_internet_gateway,
)


class TestInternetGateway(unittest.TestCase):

    @moto.mock_ec2
    def test_create_internet_gateway(self):
        ec2_client = boto3.client('ec2')

        vpc = create_vpc(name='Test', cidr_block='10.0.0.0/16')

        internet_gateway = create_internet_gateway(name='TestGateway', vpc_id=vpc.id)

        internet_gateways = ec2_client.describe_internet_gateways(InternetGatewayIds=[internet_gateway.id])['InternetGateways']
        found_internet_gateway = internet_gateways[0]

        self.assertEqual(internet_gateway.id, found_internet_gateway['InternetGatewayId'])
        self.assertEqual(internet_gateway.attachments[0]['VpcId'], found_internet_gateway['Attachments'][0]['VpcId'])

    @moto.mock_ec2
    def test_delete_internet_gateway(self):
        ec2_client = boto3.client('ec2')

        vpc = create_vpc(name='Test', cidr_block='10.0.0.0/16')

        internet_gateway = create_internet_gateway(name='TestGateway', vpc_id=vpc.id)

        internet_gateways = ec2_client.describe_internet_gateways(InternetGatewayIds=[internet_gateway.id])['InternetGateways']
        found_internet_gateway = internet_gateways[0]

        self.assertIn(internet_gateway.id, found_internet_gateway['InternetGatewayId'])

        delete_internet_gateway(internet_gateway_id=internet_gateway.id)

        internet_gateways = ec2_client.describe_internet_gateways()['InternetGateways']
        internet_gateway_ids = [internet_gateway['InternetGatewayId'] for internet_gateway in internet_gateways]

        self.assertNotIn(internet_gateway.id, internet_gateway_ids)
