"""This script nuke all eip resources"""

import boto3
from botocore.exceptions import EndpointConnectionError


def nuke_all_eip(logger):
    """
         ec2 function for destroy all elastic ip and
         network acl resources
    """
    # define connection
    ec2 = boto3.client('ec2')

    # Test if Elastic ip services is present in current aws region
    try:
        ec2.describe_addresses()
    except EndpointConnectionError:
        print('ec2 resource is not available in this aws region')
        return

    # List all ec2 elastic ip
    ec2_eip_list = ec2_list_eips()

    # Nuke all ec2 elastic ip
    for eip in ec2_eip_list:

        ec2.release_address(AllocationId=eip)
        logger.info("Nuke elastic ip %s", eip)


def ec2_list_eips():
    """
       Aws ec2 list elastic ips, list name of
       all network elastic ip and return it in list.
    """

    # define connection
    ec2 = boto3.client('ec2')
    response = ec2.describe_addresses()

    # Initialize ec2 elastic ip list
    ec2_eip_list = []

    # Retrieve all ec2 elastic ip Id
    for eip in response['Addresses']:

        ec2_eip = eip['AllocationId']
        ec2_eip_list.insert(0, ec2_eip)

    return ec2_eip_list