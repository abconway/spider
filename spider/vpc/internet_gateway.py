import boto3


def create_internet_gateway(name, vpc_id, environment='development'):
    ec2 = boto3.resource('ec2')

    internet_gateway = ec2.create_internet_gateway()

    internet_gateway.create_tags(
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

    internet_gateway.attach_to_vpc(VpcId=vpc_id)

    return internet_gateway


def delete_internet_gateway(internet_gateway_id):
    ec2 = boto3.resource('ec2')
    internet_gateway = ec2.InternetGateway(internet_gateway_id)

    for attachment in internet_gateway.attachments:
        internet_gateway.detach_from_vpc(VpcId=attachment['VpcId'])

    return internet_gateway.delete()
