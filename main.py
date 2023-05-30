import time
import requests
import re
import os

def addSignInLog(code,TOKEN):
    url = "https://tw-event.beanfun.com/MapleStory/api/Event/E20230523/AddSignInLog"
    data = {'InviteCode':code,
    'Token': TOKEN}
    try:
        response = requests.post(url, json=data)
        print("Send invitation.")
        time.sleep(0.1)
        if response.status_code == 200:
            result = response.json()
            if result["Code"] == 1:
                print("Check in!")
                return True
            elif result["Code"] == -1:
                print(result["Message"])
                return False
            elif result["Code"] == -2:
                print(result)
                return False
            else:
                print("Unknow code")
                return False
        else:
            print("Request fail")
            return False
    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        return False

def getText(page):
    url = f'https://forum.gamer.com.tw/C.php?page={page}&bsn=7650&snA=1025304&tnum=816'
    headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36" }
    return requests.get(url, headers = headers).text

def Prefetch(duplicate,page):
    s = getText(page)
    pattern = ".{8}-.{4}-.{4}-.{4}-.{12}"
    for invitation in re.findall(pattern, s):
        if invitation not in duplicate:
            duplicate.add(invitation)
    time.sleep(3)

def fetch(duplicate,page,TOKEN):
    s = getText(page)
    pattern = ".{8}-.{4}-.{4}-.{4}-.{12}"
    for invitation in re.findall(pattern, s):
        if invitation not in duplicate:
            duplicate.add(invitation)
            print(invitation)
            if addSignInLog(invitation,TOKEN):
                return True
    
    return False

def main():
    duplicate = set()
    print("Input your token:",end='')
    TOKEN = input().replace("'",'').replace('"','')

    
    ## fetch the exist invitation code
    print("Prefetching...")
    Prefetch(duplicate,1)
    Prefetch(duplicate,99999)

    while True:
        print("Wait for new code...")
        flag = False
        ## request the last page
        flag = fetch(duplicate,99999,TOKEN)
        time.sleep(3)
        ## request the first page
        flag = fetch(duplicate,1,TOKEN) or flag
        if flag:
            print("Goodbye~")
            os.system("PAUSE")
            break

        time.sleep(3)

if __name__ == '__main__':
    main()