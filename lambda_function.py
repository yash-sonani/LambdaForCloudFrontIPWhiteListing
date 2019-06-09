import boto3
import json

from Support import  validate_content, get_ranges_for_service, update_security_groups

# Name of the service, as seen in the ip-groups.json file, to extract information for
SERVICE = "CLOUDFRONT"
REGION  = "GLOBAL"

# Ports your application uses that need inbound permissions from the service for 
INGRESS_PORTS = [{'Port': 80 },{'Port': 443 }]

# Tags which identify the security groups you want to update [ Tag AutoUpdate and Protocol is not mandetory to add. Add if it is present in your SG ]
SECURITY_GROUPS = [{'Name': 'Test','AutoUpdate': 'true','Protocol' : 'http' },{'Name': 'Test2','AutoUpdate': 'true' , 'Protocol' : 'https' }]

def lambda_handler(event, context):
    
    print("Received event: " + json.dumps(event, indent=2))
    
    message = json.loads(event['Records'][0]['Sns']['Message'])
    
    # Validate Data from SNS Event
    data = json.loads(validate_content(message['url'], message['md5']))
    
    # extract the service ranges
    global_cf_ranges = get_ranges_for_service(data, SERVICE, REGION)
    
    ip_ranges = { 'GLOBAL' : global_cf_ranges}
    
    # update the security groups
    result = update_security_groups(ip_ranges,SECURITY_GROUPS,INGRESS_PORTS)
    
    print('Result: ' , result)
