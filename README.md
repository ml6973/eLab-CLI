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
Takes a JSON file with an array of students and registers them to the database.

Usage:
```
$ register.py <JSON File>
```

Format of JSON File:
```
{
  "students": [
    {
      "userName"  : *value*,
      "email" : *email value*
    },

    ...

  ]
}
```
**Note:** This script is only looking for the mentioned fields in the above
format of the JSON file. Any extra key-value pairs in the JSON file will be
ignored by the script.

##enroll.py
Takes a JSON file as an argument.
Spins up clouds instances and adds students to a course.

Usage:
```
enroll.py <JSON File>
```

Format of JSON File:
```
{
    "students": [
        {
            "userName" : *value*
        },

        ...

    ],

    "image" : *image value*,
    "cloud" : *cloud value*
}
```
**Note:** This script is only looking for the mentioned fields in the above
format of the JSON file. Any extra key-value pairs in the JSON file will be
ignored by the script.

##unenroll.py
Uses an array of students and a specified image name (provided from a JSON file)
to remove students' Virtual Machines.  

Usage:
```
unenroll.py <JSON File>
```

Format of JSON File:
```
{
    "students": [
        {
            "userName" : *value*
        },

        ...

    ],

    "image" : *image value*
}
```
**Note:** This script is only looking for the mentioned fields in the above
format of the JSON file. Any extra key-value pairs in the JSON file will be
ignored by the script.
