import MySQLdb
import sys
import json
import ConfigParser
import re
import string
from validate_email import validate_email

def validateUserName(userName):
    if not userName or userName.isspace():
        print("JSON Error: userName cannot be blank")
        return False
    #if re.match(r"([a-zA-Z0-9\-\_])+\Z", userName):
    if re.search(r'[^a-zA-Z0-9\-\_]', userName):
        print("JSON Error: Username '%s' has invalid characters."
              " Only letters, numbers, dashses, and underscore is allowed"
               % userName)
        return False
    return True

def validateEmail(userName, email):
    if not email or email.isspace():
        print("JSON Error: email cannot be blank, user '%s'" % userName)
        return False
    if not validate_email(email, verify=True):
        print("JSON Error: invalid email for user '%s'" % userName)
        return False
    return True


#register <JSON>

passwordHash = "$2y$10$tIoSoR.uDxWAXyUqs8oTguY/ssvmkbHIVG9zOwOZOzoJHPBkFvgJC"

if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + "[JSON]")
    exit()

#load config file in
parser = ConfigParser.SafeConfigParser()
parser.read("CLI_config.ini")

#Verify Connections
try:
    cnx = MySQLdb.connect(host=parser.get("eLab CLI", "hostIP").strip('"'),
                          user=parser.get("eLab CLI", "userName").strip('"'),
                          passwd=parser.get("eLab CLI", "password").strip('"'),
                          db=parser.get("eLab CLI", "db").strip('"'))
except MySQLdb.Error as e:
    print("mySQL error: {}".format(e))
    exit()
except:
    print("Unexpected error with MySQL Connection: ", sys.exc_info()[0])
    exit()

cursor = cnx.cursor()


try:
    #open JSON file
    with open(sys.argv[1]) as json_data:
        students = json.load(json_data)
        #Check if 'students' array exists
        if not 'students' in students:
            print("JSON Error: Invalid JSON Data, expected array 'students'")
        else:
            for student in students['students']:
                #verify userName
                if not 'userName' in student:
                    print("JSON Error: Invalid JSON Data, missing 'userName'")
                    continue

                userName = student['userName']
                userName = userName.strip()
                if not validateUserName(userName):
                    continue

                #verify email
                if not 'email' in student:
                    print("JSON Error: Invalid JSON Data, missing 'email'")
                    continue
                email = student['email']
                email = email.strip()
                if not validateEmail(userName, email):
                    continue


                #insert into portal DB
                try:
                    #insert new user and get userId
                    cursor.execute("INSERT INTO users (userName, passwordHash) "
                                   "VALUES ('{}', '{}')"
                                   .format(userName, passwordHash))


                    #insert email for user
                    cursor.execute("INSERT INTO userdata (userId, email) "
                                   "VALUES ('{}', '{}')"
                                   .format(cursor.lastrowid, email))
                    cnx.commit()

                except MySQLdb.Error as e:
                    print("mySQL error: {}".format(e))
                except TypeError as e:
                    print("TypeError: {}".format(e))
                except:
                    print("Insert Error: ", sys.exc_info())
                    cnx.rollback()

except IOError as e:
    print("IOError: {}".format(e))
except ValueError as e:
    print("ValueError: {}".format(e))
except NameError as e:
    print("NameError: {}".format(e))
except TypeError as e:
    print("TypeError: {}".format(e))
except:
    print("Unexpected error with JSON Input: ", sys.exc_info()[0])



cnx.close()
print("end")
