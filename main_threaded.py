from colorama import Fore, init
from bs4 import BeautifulSoup

import aiofiles
import asyncio
import aiohttp

#before running for the first time remember to set your headers

headers = {}


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
                    async with aiofiles.open("data/non_AT&T_data.txt", "a") as o:
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
                    print(Fore.RED + f"{current_number} || ERROR || STATUS CODE 403 - POSSIBLE FIX: UPDATE HEADERS - IF THIS DOESNT FIX CHANGE IP AND GET NEW HEADERS")
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
