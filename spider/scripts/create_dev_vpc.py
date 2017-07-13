from ..vpc import (
    create_vpc,
    create_subnet,
    create_internet_gateway,
    create_elastic_ip,
    create_nat_gateway,
    create_route_table,
)


def create_dev_vpc():
    vpc = create_vpc(name='TestVPC', cidr_block='10.0.0.0/16')

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


if __name__ == '__main__':
    create_dev_vpc()
