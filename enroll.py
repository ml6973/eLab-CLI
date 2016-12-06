import MySQLdb
import requests
import sys
import json

if len(sys.argv) != 4:
  print("Usage:  " + sys.argv[0] + "[image_name] [cloud] [class file]")
  exit()

image_name = sys.argv[1]
cloud = sys.argv[2]
idList = list()

# cnx = MySQLdb.connect(host='127.0.0.1', db='oci_eLab', user='root', passwd=sys.argv[8])

cnx = MySQLdb.connect(host='127.0.0.1', db='oci_eLab', user='root')
cursor = cnx.cursor()

with open(sys.argv[3]) as f:
  for line in f:
    cursor = cnx.cursor()
    query = ("SELECT userId FROM Users WHERE userName = '" + line.strip() + "'")
    
    cursor.execute(query)
    
    result = cursor.fetchall()
    
    for row in result:
      idList.append(row[0])
    cursor.close()

cnx.close()

url = "http://127.0.0.1:12345/enroll/"
my_headers = {"Content-Type": 'application/json'}  

for userId in idList:  
  body = {            
    "api_uname":"webportal",
    "api_pass":"greg123",
    "external_id":userId,
    "image_name":image_name,
    "cloud":cloud
    } 

  
  json_body = json.dumps(body)  
  r = requests.post(url, json_body, headers=my_headers)  
  
  if (r.status_code == requests.codes.created):    
    print "Student " + str(userId) + " vm successfully created"  
  else:    
    print "Error with student " + str(userId)

  print(r.status_code)

exit()
