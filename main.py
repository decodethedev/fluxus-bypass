import re
import tls_client
import random
import time

linkvertise = "https://linkvertise.com/"

session = tls_client.Session(
    client_identifier="Firefox110",
    random_tls_extension_order=True
)

browser_version = random.randint(110, 115)

headers = {
    # put your own headers here !
}

link = input("Enter Key Link: ")

hwid = link.replace("https://flux.li/windows/start.php?HWID=","")

if not link.startswith("https://flux.li/windows/start.php?HWID="):
    print("Invalid link! It should look smth like this https://flux.li/windows/start.php?HWID=...")
    exit()

print(f"Got HWID: {hwid}")

key_regex = r'let content = \("([^"]+)"\);'
endpoints =  [
    {
        "url": f"https://flux.li/windows/start.php?HWID={hwid}",
        "referer": ""
    },
    {
        "url": f"https://flux.li/windows/start.php?[OFFSET_REPLACE]=false&HWID={hwid}",
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

safe_mode = False
safe_mode_inp = input ("Do you want safe mode? This will delay the time between requests so it looks like you are just manually getting the key! (yes/no): \n >")

if safe_mode_inp.lower() == "yes":
    safe_mode = True
    print("Safe mode enabled, this will delay the time between requests so it looks like you are just manually getting the key!")

for i in range (len(endpoints)):
    url = endpoints[i]["url"].replace("[OFFSET_REPLACE]", OFFSET)
    referer = endpoints[i]["referer"]

    headers["referer"] = referer
    response = session.get(
        url,
        headers=headers
    )
    
    if i == 0:
        match = re.search(r'start.php\?(.*?)=false&HWID=', response.text)
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
 
    print(f"[{i}] Response: {response.status_code} | {url} | SAFEMODE: {safe_mode}")

    if i == len(endpoints)-1: # End of the bypass
        match = re.search(key_regex, response.text)
        if match:
            content = match.group(1)
            print(f"Bypassed successfully! Code: {content}")
        else:
            with open("bypass.html", "w") as f:
                f.write(response.text)
            print("Bypassed not successfully! Code: None, response content has been written to bypass.html for debugging purposes.")
    
    if safe_mode:
        time.sleep(random.randint(4,7))

input("Press enter to exit...")
