import firebase_admin
from firebase_admin import auth
from . import database
#import database
import json
import urllib

def addAuthUser(name, email, password):
    uid = database.addUser(name, email)
    auth.create_user(uid=uid,display_name=name,email=email, password=password)

def getUserId(email):
    userRecord = auth.get_user_by_email(email)
    print(userRecord.user_metadata)
    return userRecord.uid

def signIn(email, password):
    """
    Returns None if password is wrong
    Returns uid if logged in
    """

    my_data = dict()
    my_data["email"] = email
    my_data["password"] = password
    my_data["returnSecureToken"] = True
				
    json_data = json.dumps(my_data).encode()
    headers = {"Content-Type": "application/json"}		
    request = urllib.request.Request("https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key="+"AIzaSyCrOIfhAMyWsOeMdxc2Y_tIKdQ5Lo7YkJs",
                                         data=json_data, headers=headers)
  		

    try:
        loader = urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        message = json.loads(e.read())
        print(message["error"]["message"])
        return None
    else:
        uid = json.load(loader)['localId']
        print(uid)
        return str(uid)

