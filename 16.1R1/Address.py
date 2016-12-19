import json
import Utils

sd_session = None;
sd_root_url = "https://10.206.47.58/"
sd_username = "super"
sd_password = "123juniper"

def create_address(address):
    address_url_path = sd_root_url + "/api/juniper/sd/address-management/addresses"
    header = {'Content-Type': 'application/vnd.juniper.sd.address-management.address+json;version=1;charset=UTF-8',
              'Accept': 'application/vnd.juniper.sd.address-management.address+json;version=1;q=0.01'}

    payload_json = {'address': {
        'name': address['name'],
        'description': address['description'],
        'address-type': address['address-type'],
        'host-name': address['host-name'],
        'ip-address': address['ip-address']
    }
    }
    payload = json.dumps(payload_json)
    response = sd_session.post(url=address_url_path, data=payload, headers=header, verify=False)
    if response.status_code != 200:
        print "Failed to create address [" + (address['address-type']) + "] - Error: code = %d, text = %s" % (response.status_code, response.text)
    else:
        print "Address Object [Type - " + (address['address-type']) + " ] created successfully\n",

def delete_address(id):
    global sd_root_url
    delete_path = sd_root_url + "/api/juniper/sd/address-management/addresses/delete"
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
    path = sd_root_url + "/api/juniper/sd/address-management/addresses?rows=500&include-dynamic-addresses=false"
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
    get_path = sd_root_url + "/api/juniper/sd/address-management/addresses/%s" % (id)
    get_header = {'Accept': 'application/vnd.juniper.sd.address-management.address+json;version=1;q=0.01'}
    response = sd_session.get(url=get_path, headers=get_header, verify=False)
    if response.status_code != 200:
        print "Failed to get address info - Error: code = %d, text = %s" % (response.status_code, response.text)
    else:
        print "Address Object info retrieved successfully"

    address_object = json.loads(response.text)
    return address_object

def modify_address(address, id):
    modify_path = sd_root_url + "/api/juniper/sd/address-management/addresses/%s" % (id)
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
    print "Exmaples on how to use Address related API's"

    # Login to space
    try:
        sd_session = Utils.login(sd_root_url, sd_username, sd_password)
        print "Able to login successfully"
    except Exception as exp:
        print "Error in login to space"
        print exp

    # Create Address [Type - Host]
    address_host = {}
    address_host['name'] = "address-host"
    address_host['description'] = "Host Address Type"
    address_host['address-type'] = "IPADDRESS"
    address_host['host-name'] = ""
    address_host['ip-address'] = "192.168.1.1"

    create_address(address_host)

    # Create Address [Type - Network]
    address_network = {}
    address_network['name'] = "address-network"
    address_network['description'] = "Network Address Type"
    address_network['address-type'] = "NETWORK"
    address_network['host-name'] = ""
    address_network['ip-address'] = "192.168.1.0/24"

    create_address(address_network)

    # Create Address [Type - Range]
    address_range = {}
    address_range['name'] = "address-range"
    address_range['description'] = "Range Address Type"
    address_range['address-type'] = "RANGE"
    address_range['host-name'] = ""
    address_range['ip-address'] = "192.168.1.1-192.168.1.100"

    create_address(address_range)

    # Create Address [Type - WildCard]
    address_wildcard = {}
    address_wildcard['name'] = "address-wildcard"
    address_wildcard['description'] = "WildCard Address Type"
    address_wildcard['address-type'] = "WILDCARD"
    address_wildcard['host-name'] = ""
    address_wildcard['ip-address'] = "192.168.0.0/0.0.255.255"

    create_address(address_wildcard)

    # Create Address [Type - DNS]
    address_dns = {}
    address_dns['name'] = "address-dns"
    address_dns['description'] = "DNS Address Type"
    address_dns['address-type'] = "DNS"
    address_dns['host-name'] = "www.google.com"
    address_dns['ip-address'] = ""

    create_address(address_dns)


    # Modify Address

    # First we need to get the contents of address that needs to be modified.
    # Get all address objects and check for matching name to get the exact identifier of the object

    address_id_host = get_address_id('address-host')
    address_id_network = get_address_id('address-network')
    address_id_range = get_address_id('address-range')
    address_id_wildcard = get_address_id('address-wildcard')
    address_id_dns = get_address_id('address-dns')

    # Get complete details of relevant object

    address_object = get_address_object(address_id_host)

    # Now modify using the id retrieved earlier. Make sure edit-version field is retained and not modified.

    address_object['address']['ip-address'] = '192.169.1.1'
    address_object['address']['description'] = 'modified address host'

    modify_address(address_object, address_id_host)


    # Delete address
    delete_address(address_id_host)
    delete_address(address_id_network)
    delete_address(address_id_range)
    delete_address(address_id_wildcard)
    delete_address(address_id_dns)

    # Logout from Space.
    Utils.logout(sd_root_url, sd_session)




