from boto3 import client

SAMPLE_INSTANCE_DATA = {
    'Instances': [
        {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-53d13a927070628de', 'Type': 'a1.2xlarge',
         'ImageId': 'ami-03cf127a',
         'LaunchTime': '2020-10-13T19:27:52.000Z', 'State': 'running',
         'StateReason': None, 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
         'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
         'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
         'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
         'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
         'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
         'Tags': [{'Key': 'Name', 'Value': 'Jenkins Master'}]
         },
        {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-23a13a927070342ee', 'Type': 't2.medium',
         'ImageId': 'ami-03cf127a',
         'LaunchTime': '2020-10-18T21:27:49.000Z', 'State': 'Stopped',
         'StateReason': 'Client.UserInitiatedShutdown: User initiated shutdown', 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
         'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
         'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
         'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
         'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
         'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
         'Tags': [{'Key': 'Name', 'Value': 'Consul Node'}]
         },
        {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-77z13a9270708asd', 'Type': 't2.xlarge',
         'ImageId': 'ami-03cf127a',
         'LaunchTime': '2020-10-18T21:27:49.000Z', 'State': 'Running',
         'StateReason': None, 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
         'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
         'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
         'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
         'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
         'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
         'Tags': [{'Key': 'Name', 'Value': 'Grafana'}]
         }
    ]
}


def get_state_reason(instance):
    instance_state = instance['State']['Name']
    if instance_state != 'running':
        return instance['StateReason']['Message']


class InstanceData:
    eran = 0

    def __init__(self, ec2_client: client):
        self.ec2_client = ec2_client

    def get_instances(self):
        # TODO: The below JSON should be populated using real instance data (instead of the SAMPLE_INSTANCE_DATA)
        #       The format of SAMPLE_INSTANCE_DATA (field names and JSON structure)
        #       must be kept in order to be properly displayed in the application UI
        #
        #       Notice that when the machine is running the "StateReason" filed should be set to None
        #       and will not be shown in the UI
        #
        #       NOTE: the `self.ec2_client` is an object that is returned from doing `boto3.client('ec2')` as you can
        #       probably find in many examples on the web
        #       To read more on how to use Boto for EC2 look for the original Boto documentation
        dResponse = self.ec2_client.describe_instances()
        lReservations = dResponse['Reservations']
        lInstances = []
        lRequiredKeys = [
            'Cloud', 'Region', 'ImageId', 'LaunchTime', 'State', 'SubnetId',
            'VpcId', 'MacAddress', 'NetworkInterfaceId', 'PrivateDnsName', 'PrivateIpAddress', 'PublicDnsName',
            'PublicIpAddress', 'RootDeviceName', 'RootDeviceType', 'SecurityGroups', 'Tags',
        ]
        for reservation in lReservations:
            dInstance = reservation['Instances'][0]

            dict_variable = {}

            for key in lRequiredKeys:
                dict_variable[key] = None

            dict_variable = {key: value for (key, value) in dInstance.items() if key in lRequiredKeys}

            dict_variable['Cloud'] = 'aws'
            dict_variable['Region'] = 'us-east-1'
            dict_variable['Type'] = dInstance['InstanceType']
            dict_variable['StateReason'] = None

            for interface in dInstance['NetworkInterfaces']:
                dict_variable['MacAddress'] = (interface['MacAddress'])
                dict_variable['NetworkInterfaceId'] = (interface['NetworkInterfaceId'])

                for privateIpAddress in interface['PrivateIpAddresses']:
                    if 'PublicIp' in privateIpAddress:
                        dict_variable['PublicIpAddress'] = (privateIpAddress['PublicIp'])
                break

            if 'IamInstanceProfile' in dInstance:
                dict_variable['Id'] = dInstance['IamInstanceProfile']['Id']

            lInstances.append(dict_variable)

        return {'Instances': lInstances}

