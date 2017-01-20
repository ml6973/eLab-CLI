import MySQLdb
import sys
import json
import ConfigParser
import re
import string
import os.path
from validate_email import validate_email

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

def validateEmail(userName, email):
    #Check if email is empty or blank
    if not email or email.isspace():
        print("JSON Warning: email cannot be blank, user '%s'" % userName)
        return False

    #Check if the email actually exists
    if not validate_email(email, verify=True):
        print("JSON Warning: invalid email for user '%s'" % userName)
        return False
    return True


#register <JSON>

configFileName = "CLI_config.ini"
studentsSuccess = 0
studentsFail = 0
studentsDuplicates = 0
passwordHash = "$2y$10$tIoSoR.uDxWAXyUqs8oTguY/ssvmkbHIVG9zOwOZOzoJHPBkFvgJC"

if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " <JSON File>")
    exit()

#load config file in
if not os.path.isfile(configFileName):
    print("Config Error: Missing config file, {}".format(configFileName))
    exit()
parser = ConfigParser.SafeConfigParser()
parser.read(configFileName)

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
            raise TypeError('Invalid JSON Data, expected array "students"')
        else:
            for student in students['students']:
                #verify userName
                if not 'userName' in student:
                    studentsFail += 1
                    print("JSON Warning: Invalid JSON Data, missing 'userName'")
                    continue

                userName = student['userName']
                userName = userName.strip()
                if not validateUserName(userName):
                    studentsFail += 1
                    continue

                #verify email
                if not 'email' in student:
                    studentsFail += 1
                    print("JSON Warning: Invalid JSON Data, missing 'email'")
                    continue
                email = student['email']
                email = email.strip()
                if not validateEmail(userName, email):
                    studentsFail += 1
                    continue


                #insert into portal DB
                try:
                    #insert new user and get userId
                    cursor.execute("INSERT INTO Users (userName, passwordHash) "
                                   "VALUES ('{}', '{}')"
                                   .format(userName, passwordHash))


                    #insert email for user
                    cursor.execute("INSERT INTO UserData (userId, email) "
                                   "VALUES ('{}', '{}')"
                                   .format(cursor.lastrowid, email))
                    cnx.commit()
                    studentsSuccess += 1

                except MySQLdb.Error as e:
                    if e[0] == 1062:
                        studentsDuplicates += 1
                    print("mySQL error: {}".format(e))
                except TypeError as e:
                    print("TypeError: {}".format(e))
                except:
                    print("Insert Error: ", sys.exc_info())
                    cnx.rollback()
        print("\n{} students registered successfully. "
              "{} students failed to register. "
              "{} students already registered.".format(studentsSuccess,
              studentsFail, studentsDuplicates))

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
finally:
    cnx.close()




#print("end")
