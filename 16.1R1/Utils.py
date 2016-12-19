import base64
import requests

def login(root_url, user_name, password):
    # Root URL should be like : "https://space-ip"
    session = requests.session()
    bstr = user_name + ':' + password
    auth = base64.b64encode(bytes(bstr), 'utf-8')
    auth = auth.decode('utf-8')
    URL = root_url + '/api/space/user-management/login'
    headers = {'Authorization': 'Basic ' + auth}
    response = session.post(url=URL, headers=headers, verify=False)

    if response.status_code == 200:
        return session
    else:
        raise Exception("Error: code = %d, text = %s" % (response.status_code, response.text))

def logout(root_url, session):
    URL = root_url + '/api/space/user-management/logout'
    response = session.post(url=URL, verify=False)

    if response.status_code == 200:
        print "Logout Successful"
    else:
        raise Exception("Error: code = %d, text = %s" % (response.status_code, response.text))