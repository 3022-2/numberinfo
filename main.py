from main_threaded import start
from colorama import Fore, init
from bs4 import BeautifulSoup

import requests
import time
import os

#before running for the first time remember to set your headers

headers = {
    "authority": "www.reversephonelookup.com",
    "method": "GET",
    "path": "/number/7149967004/",
    "scheme": "https",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Cookie": "device-id=535305ac-4101-4823-a6d7-bf3ec6fc67b1; _gcl_au=1.1.199284598.1708454405; last-known-device-id=535305ac-4101-4823-a6d7-bf3ec6fc67b1; PHPSESSID=6kvi0agg73qp23s1uk7n5r9p7g; sessionId=559bb42f-bdee-4f63-bb6a-d98880ca708c; sessionCreated=2024-03-05T21%3A20%3A12%2B00%3A00; _gid=GA1.2.1592401715.1709673614; cf_clearance=udXI1x_jpI_ommg7XM8KwyiLvpY.UU399kersDS_AfM-1709673614-1.0.1.1-10FYKtfVreeyRgw9JlHZFHaD6WscWO1FHVAzKijXbnV6LzxEzs728Rj5B0W8ev9lv_hx_VpT.hFEV4nZZ3DpSw; _ga_0V7NXWZ64P=GS1.1.1709673614.22.1.1709674256.50.0.0; _ga=GA1.2.707113878.1708454406",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

cwd = os.getcwd()

init(autoreset=True)

def request_sites(current_number):
    def reversephonelookup(current_number):
        r = requests.get(f"https://www.reversephonelookup.com/number/{current_number}/", headers=headers)
        try:
            if "Access your full phone report and unlock all associated data." and "ReversePhoneLookup.com" and "AT&T" in r.text:
                print(Fore.GREEN + f"{current_number} || VALID || AT&T")
                soup = BeautifulSoup(r.text, 'html.parser')
                ownername = soup.find("h3")
                generalinfo = soup.find("ul")
                if generalinfo and ownername:
                    with open("data/AT&T_data.txt", "a") as o:
                        if ownername and generalinfo:
                            owner_name = ownername.get_text().strip()
                            o.write(f"{current_number} - {owner_name}\n")
                            
                            address = carrier = None
                            for li in generalinfo.find_all("li"):
                                text = li.get_text().strip()
                                if text.startswith(" "):
                                    address = text
                                elif text.startswith("Carrier Type"):
                                    carrier = text.split(":")[1].strip()
                            if address:
                                o.write(f"{address}\n")
                            if carrier:
                                o.write(f"{carrier}\n")
                                o.write("------------------------\n")
                else:
                    print(Fore.RED + f"{current_number} || Element not found.")

            elif "Access your full phone report and unlock all associated data." and "ReversePhoneLookup.com" in r.text:
                print(Fore.YELLOW + f"{current_number} || SEMI-VALID || NOT AT&T")
                soup = BeautifulSoup(r.text, 'html.parser')
                ownername = soup.find("h3")
                generalinfo = soup.find("ul")
                if generalinfo and ownername:
                    with open("data/non_AT&T_data.txt", "a") as o:
                        if ownername and generalinfo:
                            owner_name = ownername.get_text().strip()
                            o.write(f"{current_number} - {owner_name}\n")
                            
                            address = carrier = None
                            for li in generalinfo.find_all("li"):
                                text = li.get_text().strip()
                                if text.startswith(" "):
                                    address = text
                                elif text.startswith("Carrier Type"):
                                    carrier = text.split(":")[1].strip()
                            
                            if address:
                                o.write(f"{address}\n")
                            if carrier:
                                o.write(f"{carrier}\n")
                                o.write("------------------------\n")
                else:
                    print(Fore.RED + f"{current_number} || Element not found.")
            else:
                if r.status_code == 403:
                    print(Fore.RED + f"{current_number} || ERROR || STATUS CODE 403 - POSSIBLE FIX: UPDATE HEADERS - IF THIS DOESNT FIX CHANGE IP AND GET NEW HEADERS")
                else:
                    print(Fore.RED + f"{current_number} || INVALID || DOESNT EXIST")        
        except Exception as e:
                    print(Fore.RED + e)
    reversephonelookup(current_number)

def random_generate():
    def generate_numbers(input_number):
        num_zeros = len(input_number) - len(input_number.rstrip('0'))
        
        upper_bound = int(input_number) + 10**num_zeros - 1
        
        current_number = int(input_number)
        while current_number <= upper_bound:

            request_sites(current_number)
            current_number += 1
        
    input_number = input("Enter a 10-digit number (e.g: 3343670000): ")

    if len(input_number) != 10 or not input_number.isdigit():
        print(Fore.RED + "Invalid input! Please enter a 10-digit number.")
    else:
        generate_numbers(input_number)

def fromlist():
    with open("phonenumbers.txt", "r") as o:
        for current_number in o:
            request_sites(current_number.strip())       

def main():
    print(Fore.RED + """
1. Method - unthreaded - slow
2. Method - threaded - fast
0. Quit
""")
    
    choice = int(input(Fore.GREEN + ">>"))

    if choice == 1: 
        print(Fore.RED + """
1. Randomly generate US phone numbers (1 requests / second)
2. Load phone numbers from txt (1 requests / second)
0. Quit
""")
        choice = int(input(Fore.GREEN + ">>"))

        if choice == 1:
            random_generate()
        elif choice == 2:
            fromlist()
        elif choice == 0:
            exit()
        else:
            print(Fore.RED + f"{choice} isnt an option")
            time.sleep(1)
            main()
    elif choice == 2:
        start()
    elif choice == 0:
        exit()
    else:
        print(Fore.RED + f"{choice} is not an option")
        time.sleep(1)
        main()
if __name__ == "__main__":
    print(Fore.RED + """
███╗   ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗██████╗ ██╗███╗   ██╗███████╗ ██████╗ 
████╗  ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔══██╗██║████╗  ██║██╔════╝██╔═══██╗
██╔██╗ ██║██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝██║██╔██╗ ██║█████╗  ██║   ██║
██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗██║██║╚██╗██║██╔══╝  ██║   ██║
██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║██║██║ ╚████║██║     ╚██████╔╝
╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ 
""")
    
    print(Fore.RED + "RED = INVALID - Number doesnt exist")
    print(Fore.YELLOW + "YELLOW = SEMI-VALID - Phone number exists but not carried by AT&T")
    print(Fore.GREEN + "GREEN = VALID - Phone number exists and is carried by AT&T")
    print("")
    print(Fore.MAGENTA + "DONT FORGET TO RESET THE HEADERS BEFORE EVERY USE")

    main()