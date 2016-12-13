# eLab-CLI
Contains the CLI Tools for eLab

Install Python 2.6 Dependencies:
```
$ sudo apt-get update
$ sudo apt-get install python-pip
$ sudo apt-get install python-dev libmysqlclient-dev
$ sudo pip install MySQL-python
$ sudo pip install requests
$ sudo pip install validate_email
$ sudo pip install pyDNS
```

##register.py
Takes a Json file with an array of students and registers them to the database.

Usage:
```
$ register.py [JSON File]
```