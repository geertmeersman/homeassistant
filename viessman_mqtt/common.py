import requests
import json
import configuration

def getToken():
    global vToken

    authorizeURL = 'https://iam.viessmann.com/idp/v1/authorize';
    token_url = 'https://iam.viessmann.com/idp/v1/token';
    apiURLBase = 'https://api.viessmann-platform.io';
    callback_uri = "vicare://oauth-callback/everest";

#Settings to request Autorization Code
    url = authorizeURL + "?client_id=" + configuration.viessmann['client_id'] + "&scope=openid&redirect_uri=" + callback_uri + "&response_type=code";

    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    #Try to get a response, but the requests library does not allow a request URL that does not start with http (ours is: "vicare://oauth-callback/everest")
    try:
        response = requests.post(url, headers=header, auth=(configuration.viessmann['login'], configuration.viessmann['password']))
    except Exception as e:
        #capture the error, which contains the code the authorization code and put this in to codestring
        codestring = "{0}".format(str(e.args[0])).encode("utf-8");
        codestring = str(codestring)
        codestring = codestring[codestring.find("?code=")+6:len(codestring)-1]
        #print(codestring)

#Use autorization code to request access_token
    header = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    data = {
      'client_id':configuration.viessmann['client_id'],
      'code':codestring,
      'redirect_uri':callback_uri,
      'grant_type':'authorization_code',
    }
    response = requests.post(token_url, headers=header, data=data, auth=(configuration.viessmann['client_id'], configuration.viessmann['client_secret']))
    data = response.json()
    vToken = data["access_token"]

def SetData(ReqURL, Token, feature, action, data):
    #Define Request header
    header = {
     'Authorization':'Bearer ' + Token,
     'Content-Type':'application/json'
     }
    response = requests.post(ReqURL+'heating.circuits.0.'+feature+'/'+action, headers=header, data=json.dumps(data))
    return response

#SubRoutine for requests
def GetData(ReqURL, Token, returnValue):
    #Define Request header
    header = {
     'Authorization':'Bearer ' + Token,
     'Cache-Control': 'no-cache'
     }
    #Get RequestURL with header

    response = requests.get(ReqURL+returnValue, headers=header)
    data = response.json()
#    print data
    if not returnValue:
        return data
    ret = {}
    if "message" in data and data["message"] == "FEATURE_NOT_FOUND":
        return
    if not any(data["properties"]):
        return
    if "value" in data["properties"]:
        ret['value'] = data["properties"]["value"]["value"]
    if "status" in data["properties"]:
        ret['status'] = data["properties"]["status"]["value"]
    if "active" in data["properties"]:
        ret['active'] = data["properties"]["active"]["value"]
    if "slope" in data["properties"]:
        ret['slope'] = data["properties"]["slope"]["value"]
    if "enabled" in data["properties"]:
        ret['enabled'] = data["properties"]["enabled"]["value"]
    if "entries" in data["properties"]:
        ret['entries'] = data["properties"]["entries"]["value"]
    if "temperature" in data["properties"]:
        ret['temperature'] = data["properties"]["temperature"]["value"]
    if not any(ret):
        print data
        return
    #Return response as JSON
    #print("{0} | {1}").format(returnValue, ret)
    return ret;

def GetVData(feature):
    return GetData(URL, vToken, feature)

def SetVData(feature, action, data):
    return SetData(URL, vToken, feature, action, data);

apiURLBase = 'https://api.viessmann-platform.io';
apiURL = apiURLBase + '/general-management/installations?expanded=true&'

vToken = ""
getToken();
data = GetData(apiURL, vToken, '')
if "entities" not in data:
  exit()
ID = data["entities"][0]["properties"]["id"] #ID of the installation
SERIAL = data["entities"][0]["entities"][0]["properties"]["serial"] #Serial of installation
#Combine ID & SERIAL into URL to get data out
URL = apiURLBase + '/operational-data/installations/' + str(ID) + '/gateways/' + str(SERIAL) + '/devices/0/features/'
