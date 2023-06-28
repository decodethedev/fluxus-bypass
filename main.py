import requests
import re

linkvertise = "https://linkvertise.com/"

headers = {
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
}

link = input("Enter Key Link: ")

hwid = link.replace("https://flux.li/windows/start.php?HWID=","")

print(f"Got HWID: {hwid}")

key_regex = r'let content = \("([^"]+)"\);'
endpoints =  [
    {
        "url": f"https://flux.li/windows/start.php?HWID={hwid}",
        "referer": ""
    },
    {
        "url": f"https://flux.li/windows/start.php?[OFFSET_REPLACE]=true&HWID={hwid}",
        "referer": f"https://flux.li/windows/start.php?HWID={hwid}"
    },
    {
        "url": "https://fluxteam.net/windows/checkpoint/check1.php",
        "referer": linkvertise
    },
    {
        "url": "https://fluxteam.net/windows/checkpoint/check2.php",
        "referer": linkvertise
    },
    {
        "url": "https://fluxteam.net/windows/checkpoint/main.php",
        "referer": linkvertise
    },
]

OFFSET = ""

for i in range (len(endpoints)):
    url = endpoints[i]["url"].replace("[OFFSET_REPLACE]", OFFSET)
    referer = endpoints[i]["referer"]

    headers["referer"] = referer
    response = requests.get(url, headers=headers)
    
    if i == 0:
        match = re.search(r'start.php\?(.*?)=true&HWID=', response.text)
        if match:
            OFFSET = match.group(1)
        else:
            print("Fluxus has patched the bypass, wait for a fix from the developer.")
            with open("bypass.html", "w") as f:
                f.write(response.text)
            exit()

    if response.status_code != 200:
        with open("bypass.html", "w") as f:
            f.write(response.text)
        print(f"[{i}] Failed to bypass | Status code: {response.status_code}| Response content has been written to bypass.html for debugging purposes.")

    print(f"[{i}] Response: {response.status_code} | {url}")

    if i == len(endpoints)-1: # End of the bypass
        match = re.search(key_regex, response.text)
        if match:
            content = match.group(1)
            print(f"Bypassed successfully! Code: {content}")
        else:
            with open("bypass.html", "w") as f:
                f.write(response.text)
            print("Bypassed not successfully! Code: None, response content has been written to bypass.html for debugging purposes.")
        
        