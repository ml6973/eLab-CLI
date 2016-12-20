import MySQLdb
import requests
import sys
import json
import ConfigParser
import os.path
import re

def validateUserName(userName):
    #Check if userName is empty or blank
    if not userName or userName.isspace():
        print("JSON Warning: userName cannot be blank")
        return False

    #Check for invaid characters
    if re.search(r'[^a-zA-Z0-9\-\_]', userName):
        print("JSON Warning: Username '%s' has invalid characters."
              " Only letters, numbers, dashses, and underscores is allowed"
               % userName)
        return False
    return True

#enroll script main
if len(sys.argv) != 2:
    print("Usage:  " + sys.argv[0] + " <JSON File>")
    exit()

configFileName = "CLI_config.ini"

image_name = None
cloud = None
idList = set()

#load config file in
if not os.path.isfile(configFileName):
    print("Config Error: Missing config file, {}".format(configFileName))
    exit()

parser = ConfigParser.SafeConfigParser()
parser.read(configFileName)

try:
    #Get connection to db
    cnx = MySQLdb.connect(host=parser.get("eLab CLI", "hostIP").strip('"'),
                          user=parser.get("eLab CLI", "userName").strip('"'),
                          passwd=parser.get("eLab CLI", "password").strip('"'),
                          db=parser.get("eLab CLI", "db").strip('"'))
    cursor = cnx.cursor()
except MySQLdb.Error as e:
    print("mySQL error: {}".format(e))
    exit()
except:
    print("Unexpected error with MySQL Connection: ", sys.exc_info()[0])
    exit()

try:
    #load in the json file
    with open(sys.argv[1]) as f:
        json_data = json.load(f)
        #Check if 'students' array exists
        if not 'students' in json_data:
            raise TypeError('Invalid JSON Data, expected array "students"')
        #Get the ids of the students
        for student in json_data['students']:
            #verify userName
            if not 'userName' in student:
                #studentsFail += 1
                print("JSON Warning: Invalid JSON Data, missing 'userName'")
                continue

            userName = student['userName']
            userName = userName.strip()
            if not validateUserName(userName):
                #studentsFail += 1
                continue

            query = ("SELECT userId FROM Users WHERE userName = '" + userName
                     + "'")

            cursor.execute(query)

            result = cursor.fetchone()
            if result:
              idList.add(result[0])
        cursor.close()

        #load in image_name
        if not 'image' in json_data:
            raise TypeError('Invalid JSON Data, expected array "image"')
        image_name = json_data['image']
        image_name = image_name.strip()

        if not image_name or image_name.isspace():
            raise ValueError("Invalid JSON Data: image cannot be blank")

        if not isinstance(image_name, basestring):
            raise ValueError("Invalid JSON Data: image must be a string")

        #load in cloud
        if not 'cloud' in json_data:
            raise TypeError('Invalid JSON Data, expected array "cloud"')
        cloud = json_data['cloud']
        cloud = cloud.strip()

        if not cloud or cloud.isspace():
            raise ValueError("Invalid JSON Data: cloud cannot be blank")

        if not isinstance(cloud, basestring):
            raise ValueError("Invalid JSON Data: cloud must be a string")

    cnx.close()
except MySQLdb.Error as e:
    print("mySQL error: {}".format(e))
    exit()
except:
    print("Unexpected error: ", sys.exc_info())
    exit()

url = ("http://" + parser.get("eLab CLI", "APIHostIP").strip('"') + ":"
      + parser.get("eLab CLI", "APIhostPort").strip('"') + "/enroll/")
my_headers = {"Content-Type": 'application/json'}

for userId in idList:
    body = {
        "api_uname":parser.get("eLab CLI", "APIUserName").strip('"'),
        "api_pass":parser.get("eLab CLI", "APIPassword").strip('"'),
        "external_id":userId,
        "image_name":image_name,
        "cloud":cloud
    }

    try:
          json_body = json.dumps(body)
          r = requests.post(url, json_body, headers=my_headers)

          if (r.status_code == requests.codes.created):
            print "Student " + str(userId) + " vm successfully created"
          else:
            print "Error with student " + str(userId)

          print(r.status_code)
    except:
        print("Unexpected error: ", sys.exc_info()[0])

exit()
