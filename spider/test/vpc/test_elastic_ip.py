import unittest

import boto3
import moto

from spider.vpc import (
    create_elastic_ip,
    delete_elastic_ip,
)


class TestElasticIP(unittest.TestCase):

    @moto.mock_ec2
    def test_create_elastic_ip(self):
        ec2_client = boto3.client('ec2')

        elastic_ip = create_elastic_ip()

        elastic_ips = ec2_client.describe_addresses()['Addresses']
        elastic_ips_allocation_ids = [eip['AllocationId'] for eip in elastic_ips]

        self.assertIn(elastic_ip['AllocationId'], elastic_ips_allocation_ids)

    @moto.mock_ec2
    def test_delete_elastic_ip(self):
        ec2_client = boto3.client('ec2')

        elastic_ip = create_elastic_ip()

        elastic_ips = ec2_client.describe_addresses()['Addresses']
        elastic_ips_allocation_ids = [eip['AllocationId'] for eip in elastic_ips]

        self.assertIn(elastic_ip['AllocationId'], elastic_ips_allocation_ids)

        delete_elastic_ip(elastic_ip['AllocationId'])

        elastic_ips = ec2_client.describe_addresses()['Addresses']
        elastic_ips_allocation_ids = [eip['AllocationId'] for eip in elastic_ips]

        self.assertNotIn(elastic_ip['AllocationId'], elastic_ips_allocation_ids)
