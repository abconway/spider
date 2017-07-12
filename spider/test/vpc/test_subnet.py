import unittest

import boto3
import moto

from spider.vpc import (
    create_vpc,
    create_subnet,
    delete_subnet,
)


class TestSubnet(unittest.TestCase):

    @moto.mock_ec2
    def test_create_subnet(self):
        ec2_client = boto3.client('ec2')

        vpc = create_vpc(name='Test', cidr_block='10.0.0.0/16')

        subnet = create_subnet(
            name='TestSubnet',
            vpc_id=vpc.id,
            cidr_block='10.0.0.0/19',
            availability_zone='us-east-1a',
        )

        subnets = ec2_client.describe_subnets(SubnetIds=[subnet.id])['Subnets']
        found_subnet = subnets[0]

        self.assertEqual(subnet.id, found_subnet['SubnetId'])
        self.assertEqual(subnet.cidr_block, found_subnet['CidrBlock'])
        self.assertEqual(subnet.availability_zone, found_subnet['AvailabilityZone'])

    @moto.mock_ec2
    def test_delete_subnet(self):
        ec2_client = boto3.client('ec2')

        vpc = create_vpc(name='Test', cidr_block='10.0.0.0/16')

        subnet = create_subnet(
            name='TestSubnet',
            vpc_id=vpc.id,
            cidr_block='10.0.0.0/19',
            availability_zone='us-east-1a',
        )

        subnets = ec2_client.describe_subnets(SubnetIds=[subnet.id])['Subnets']
        found_subnet = subnets[0]

        self.assertEqual(subnet.id, found_subnet['SubnetId'])

        delete_subnet(subnet_id=subnet.id)

        subnets = ec2_client.describe_subnets(SubnetIds=[subnet.id])['Subnets']

        self.assertEqual(len(subnets), 0)
