import boto3
import hashlib
from urllib.request import urlopen


from SG_Operation import update_security_group

# This functio check content with MD5 hash value

def validate_content(url, expected_hash):

    response = urlopen(url)
    
    data = response.read()

    m = hashlib.md5()
    m.update(data)
    hashValue = m.hexdigest()

    if hashValue != expected_hash:
        raise Exception('MD5 Mismatch: got ' + hashValue + ' expected ' + expected_hash)

    return data

# This Function get All IP Addesses (IPv4)
    
def get_ranges_for_service(ranges, service, subset):
    service_ranges = list()
    for prefix in ranges['prefixes']:
        if prefix['service'] == service and ((subset == prefix['region'] and subset == "GLOBAL") or (subset != 'GLOBAL' and prefix['region'] != 'GLOBAL')):
            service_ranges.append(prefix['ip_prefix'])
    
    return service_ranges
    

def update_security_groups(new_ranges,SECURITY_GROUPS,INGRESS_PORTS):
    client = boto3.client('ec2')

    # Process Every SG with Provided Ingress Ports
    
    for index,SG in enumerate(SECURITY_GROUPS):
                
        IN_PORT = INGRESS_PORTS[index]
        
        security_group_list = get_security_groups_for_update(client,SG)
        
        result = list()
    
        entries_updated = 0

        for group in security_group_list:
            if update_security_group(client, group, new_ranges['GLOBAL'], IN_PORT['Port']):
                entries_updated += 1
                result.append('Updated ' + group['GroupId'])
                
        print('Total Entries Updated: ' , entries_updated)

    return result
    
# This Function Find Security Group having security_group_tag
    
def get_security_groups_for_update(client, security_group_tag):
    filters = list();
    for key, value in security_group_tag.items():
        filters.extend(
            [
                { 'Name': "tag-key", 'Values': [ key ] },
                { 'Name': "tag-value", 'Values': [ value ] }
            ]
        )

    response = client.describe_security_groups(Filters=filters)

    return response['SecurityGroups']
