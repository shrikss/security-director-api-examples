import json
import Utils
import space_details

sd_session = None

def buildAddressGroupString(address_name_list):
    addrGroupStringStart = '{"member":['
    addrGroupStringEnd = ']}'

    addrGroupString = addrGroupStringStart
    for address_name in address_name_list:
        memberString = "{\"name\": \"%s\", \"id\": %d }," % (address_name, get_address_id(address_name))
        print memberString
        addrGroupString = addrGroupString + memberString

    print addrGroupString
    addrGroupString = addrGroupString[:-1]
    addrGroupString = addrGroupString + addrGroupStringEnd
    return addrGroupString

def create_address(address):
    address_url_path = space_details.sd_root_url + "/api/juniper/sd/address-management/addresses"
    header = {'Content-Type': 'application/vnd.juniper.sd.address-management.address+json;version=1;charset=UTF-8',
              'Accept': 'application/vnd.juniper.sd.address-management.address+json;version=1;q=0.01'}

    payload_json = {'address': {
        'name': address['name'],
        'description': address['description'],
        'address-type': address['address-type'],
        'host-name': address['host-name'],
        'address-version' : address['address-version'],
        'ip-address': address['ip-address']
        }
    }
    payload = json.dumps(payload_json)
    response = sd_session.post(url=address_url_path, data=payload, headers=header, verify=False)
    if response.status_code != 200:
        print "Failed to create address [" + (address['address-type']) + "] - Error: code = %d, text = %s" % (response.status_code, response.text)
    else:
        print "Address Object [Type - " + (address['address-type']) + " ] created successfully\n",

def create_address_group(address):
    address_url_path = space_details.sd_root_url + "/api/juniper/sd/address-management/addresses"
    header = {'Content-Type': 'application/vnd.juniper.sd.address-management.address+json;version=1;charset=UTF-8',
              'Accept': 'application/vnd.juniper.sd.address-management.address+json;version=1;q=0.01'}

    payload_json = {"address": {
        "name": address['name'],
        "description": address['description'],
        "address-type": address['address-type'],
        "members": json.loads(address['members'])
        }
    }

    payload = json.dumps(payload_json)
    response = sd_session.post(url=address_url_path, data=payload, headers=header, verify=False)
    if response.status_code != 200:
        print "Failed to create address [" + (address['address-type']) + "] - Error: code = %d, text = %s" % (response.status_code, response.text)
    else:
        print "Address Object [Type - " + (address['address-type']) + " ] created successfully\n",

def delete_address(id):
    delete_path = space_details.sd_root_url + "/api/juniper/sd/address-management/addresses/delete"
    header = {'Content-Type': 'application/vnd.juniper.sd.bulk-delete+json;version=1;charset=UTF-8'}
    list_id = list()
    list_id.append(id)
    input_data = {"id-list": {"ids": []}}
    input_data['id-list']['ids'] = list_id
    payload = json.dumps(input_data)
    global sd_session
    response = sd_session.post(url=delete_path, data=payload, headers=header, verify=False)
    if response.status_code != 204:
        print "Failed to delete address - Error: code = %d, text = %s" % (response.status_code, response.text)
    else:
        print "Address Object [Id: " + str(id) + "] deleted successfully"

def get_address_id(name):
    path = space_details.sd_root_url + "/api/juniper/sd/address-management/addresses?rows=500&include-dynamic-addresses=false"
    header = {'Accept': 'application/vnd.juniper.sd.address-management.address-refs+json;version=1;q=0.01'}
    response = sd_session.get(url=path, headers=header, verify=False)
    if response.status_code != 200:
        print ("Failed in getting address details Error: code = %d, text = %s" % (response.status_code, response.text))
        exit()

    address_id = None
    output = json.loads(response.text)
    for address in output['addresses']['address']:
        if (address['name'] == name):
            address_id = address['id']
            break
    return address_id

def get_address_object(id):
    get_path = space_details.sd_root_url + "/api/juniper/sd/address-management/addresses/%s" % (id)
    get_header = {'Accept': 'application/vnd.juniper.sd.address-management.address+json;version=1;q=0.01'}
    response = sd_session.get(url=get_path, headers=get_header, verify=False)
    if response.status_code != 200:
        print "Failed to get address info - Error: code = %d, text = %s" % (response.status_code, response.text)
    else:
        print "Address Object info retrieved successfully"

    address_object = json.loads(response.text)
    return address_object

def modify_address_group(address, id):
    modify_path = space_details.sd_root_url + "/api/juniper/sd/address-management/addresses/%s" % (id)
    modify_header = {
        'Content-Type': 'application/vnd.juniper.sd.address-management.address+json;version=1;charset=UTF-8',
        'Accept': 'application/vnd.juniper.sd.address-management.address+json;version=1;q=0.01'}
    address_string = json.dumps(address)
    response = sd_session.put(url=modify_path, data=address_string, headers=modify_header, verify=False)
    if response.status_code != 200:
        print "Failed to modify address - Error: code = %d, text = %s" % (response.status_code, response.text)
    else:
        print "Address Object modified successfully"

if __name__ == "__main__":
    print "Exmaples on how to use Address Group related API's"

    # Login to space
    try:
        sd_session = Utils.login(space_details.sd_root_url, space_details.sd_username, space_details.sd_password)
        print "Able to login successfully"
    except Exception as exp:
        print "Error in login to space"
        print exp

    # Create Address [Type - Host]
    address_host = {}
    address_host['name'] = "address-group-member1-host"
    address_host['description'] = "Host Address Type"
    address_host['address-type'] = "IPADDRESS"
    address_host['host-name'] = ""
    address_host['address-version'] = "IPV4"
    address_host['ip-address'] = "192.168.1.1"

    create_address(address_host)

    address_network_1 = {}
    address_network_1['name'] = "address-group-member2-network"
    address_network_1['description'] = "Network Address Type"
    address_network_1['address-type'] = "NETWORK"
    address_network_1['host-name'] = ""
    address_network_1['address-version'] = "IPV4"
    address_network_1['ip-address'] = "192.168.1.0/24"

    create_address(address_network_1)

    address_network_2 = {}
    address_network_2['name'] = "address-group-member3-network"
    address_network_2['description'] = "Network Address Type"
    address_network_2['address-type'] = "NETWORK"
    address_network_2['host-name'] = ""
    address_network_2['address-version'] = "IPV4"
    address_network_2['ip-address'] = "192.178.1.0/24"

    create_address(address_network_2)

    address_list = list()
    address_list.append("address-group-member1-host")
    address_list.append("address-group-member2-network")

    # Create Address Group
    address_group = {}
    address_group['name'] = "address-group"
    address_group['description'] = "Address Group Type"
    address_group['address-type'] = "GROUP"
    address_group['members'] = buildAddressGroupString(address_list)
    address_group['ip-address'] = "192.168.1.1"

    create_address_group(address_group)

    address_modified_list = list()
    address_modified_list.append("address-group-member1-host")
    address_modified_list.append("address-group-member3-network")

    address_group_id = get_address_id("address-group")
    address_group_object = get_address_object(address_group_id)

    address_group_object['address']['members'] = json.loads(buildAddressGroupString(address_modified_list))

    modify_address_group(address_group_object, address_group_id)

    # Delete address

    delete_address(address_group_id)
    delete_address(get_address_id("address-group-member1-host"))
    delete_address(get_address_id("address-group-member2-network"))
    delete_address(get_address_id("address-group-member3-network"))

    # Logout from Space.
    Utils.logout(space_details.sd_root_url, sd_session)




