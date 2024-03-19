from colorama import Fore, init
from bs4 import BeautifulSoup

import aiofiles
import asyncio
import aiohttp

#before running for the first time remember to set your headers

headers = {
    "authority": "www.reversephonelookup.com",
    "method": "GET",
    "path": "/number/7149967075/",
    "scheme": "https",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Cookie": "device-id=d87b4868-db09-4698-b840-037e72d88fb8; _gcl_au=1.1.67196235.1710808036; _gid=GA1.2.601514972.1710808036; last-known-device-id=d87b4868-db09-4698-b840-037e72d88fb8; cf_chl_3=3d019c99636adec; cf_clearance=b0tkjmRY0qwqcfxTp9zmaYTVO30p3XOrkQpPxkVKcAA-1710810043-1.0.1.1-W.yQaJjz6Ro3t28mi7RxqwF3HL0VC3rMF4Bovv2OSWQZFtHVzZj1x3d6WPT_pH.WROmH1jtdJZjA7hTEog8Thw; PHPSESSID=1720u598qr0j7rb71kit330rv8; sessionId=2d97c90b-49de-454a-98ea-dc31cce37f8d; sessionCreated=2024-03-19T01%3A03%3A35%2B00%3A00; _ga_0V7NXWZ64P=GS1.1.1710808036.1.1.1710810309.60.0.0; _ga=GA1.2.1972488876.1710808036; _gat_UA-74882607-7=1",
    "Sec-Ch-Ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
    "Sec-Ch-Ua-Arch": "x86",
    "Sec-Ch-Ua-Bitness": "64",
    "Sec-Ch-Ua-Full-Version": "122.0.6261.129",
    "Sec-Ch-Ua-Full-Version-List": "\"Chromium\";v=\"122.0.6261.129\", \"Not(A:Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"122.0.6261.129\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Model": "\"\"",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Ch-Ua-Platform-Version": "\"15.0.0\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0"
}



async def request_site(session, current_number):
    try:
        async with session.get(f"https://www.reversephonelookup.com/number/{current_number}/", headers=headers) as response:
            html = await response.text()
            if "Access your full phone report and unlock all associated data." and "ReversePhoneLookup.com" and "AT&T" in html:
                print(Fore.GREEN + f"{current_number} || VALID || AT&T")
                soup = BeautifulSoup(html, 'html.parser')
                ownername = soup.find("h3")
                generalinfo = soup.find("ul")
                if generalinfo and ownername:
                    async with aiofiles.open("data/AT&T_data.txt", "a") as o:
                        ownername = ownername.get_text().strip()
                        await o.write(f"{current_number} - {ownername}\n")

                        if generalinfo:
                            address = carrier = None
                            for li in generalinfo.find_all("li"):
                                text = li.get_text().strip()
                                if text.startswith(" "):
                                    address = text
                                elif text.startswith("Carrier Type"):
                                    carrier = text.split(":")[1].strip()
                            if address:
                                await o.write(f"{address}\n")
                            if carrier:
                                await o.write(f"{carrier}\n")
                                await o.write("------------------------\n")
                else:
                    print(Fore.RED + f"{current_number} || Element not found.")

            elif "Access your full phone report and unlock all associated data." and "ReversePhoneLookup.com" in html:
                print(Fore.YELLOW + f"{current_number} || SEMI-VALID || NOT AT&T")
                soup = BeautifulSoup(html, 'html.parser')
                ownername = soup.find("h3")
                generalinfo = soup.find("ul")
                if generalinfo and ownername:
                    async with aiofiles.open("data/AT&T_data.txt", "a") as o:
                        ownername = ownername.get_text().strip()
                        await o.write(f"{current_number} - {ownername}\n")
                        
                        if generalinfo:
                            address = carrier = None
                            for li in generalinfo.find_all("li"):
                                text = li.get_text().strip()
                                if text.startswith(" "):
                                    address = text
                                elif text.startswith("Carrier Type"):
                                    carrier = text.split(":")[1].strip()
                            if address:
                                await o.write(f"{address}\n")
                            if carrier:
                                await o.write(f"{carrier}\n")
                                await o.write("------------------------\n")
                else:
                    print(Fore.RED + f"{current_number} || Element not found.")
            else:
                if response.status == 403:
                    print(Fore.RED + f"{current_number} || ERROR || STATUS CODE 403 - POSSIBLE FIX: UPDATE HEADERS - IF THAT DOESNT WORK GET NEW IP")
                else:
                    print(Fore.RED + f"{current_number} || INVALID || DOESNT EXIST")        
    except Exception as e:
        print(Fore.RED + str(e))

async def random_generate(session, input_number, delay_ms):
    num_zeros = len(input_number) - len(input_number.rstrip('0'))
    upper_bound = int(input_number) + 10**num_zeros - 1
    tasks = []
    for current_number in range(int(input_number), upper_bound + 1):
        task = asyncio.ensure_future(request_site(session, str(current_number)))
        tasks.append(task)
        await asyncio.sleep(delay_ms / 1000)
    await asyncio.gather(*tasks)

async def fromlist(session, delay_ms):
    with open("phonenumbers.txt", "r") as o:
        tasks = []
        for current_number in o:
            task = asyncio.ensure_future (request_site(session, current_number.strip()))
            tasks.append(task)
            await asyncio.sleep(delay_ms / 1000)
        await asyncio.gather(*tasks)

async def main():
    print(Fore.RED + """
1. Randomly generate US phone numbers - Threaded (you choose speed)
2. Load phone numbers from txt - Threaded (you choose speed)
0. Quit
""")
    choice = int(input(Fore.GREEN + ">>"))
    if choice == 0:
        exit()
    else:
        pass
    delay_ms = int(input(Fore.GREEN + "Enter delay in milliseconds (e.g: 500 = 0.5 seconds): "))
    async with aiohttp.ClientSession() as session:
        if choice == 1:
            input_number = input(Fore.GREEN + "Enter a 10-digit number (e.g: 3343670000): ")
            if len(input_number) != 10 or not input_number.isdigit():
                print(Fore.RED + "Invalid input! Please enter a 10-digit number.")
                return
            await random_generate(session, input_number, delay_ms)
        elif choice == 2:
            await fromlist(session, delay_ms)
        else:
            print(Fore.RED + "Invalid choice")

def start():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

if __name__ == "__main__":
    start()