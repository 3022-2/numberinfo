# numberinfo

A program written in python to bulk check the owners of generated US phone numbers without using an API, Instead it uses web scraping. 
----
When running the code it says "dont forget to reset the headers before every use", this is a half truth. You only really need to reset headers if your on a new internet connection, headers being blocked, ip being blocked. Otherwise if i set headers one day and run it and then the next day set headers and run it on the same wifi it should work granted the ip/header hasnt been blocked
----
DISCLAIMER: This tool is provided for educational purposes only. I, as the creator, do not condone or support any misuse of this tool for illegal or unethical activities. It is your responsibility as a user to ensure that your use of this tool complies with all applicable laws and regulations in your jurisdiction. By using this tool, you agree that I shall not be held liable for any consequences arising from your use of the tool, including but not limited to any legal actions or damages incurred. Please use this tool responsibly and ethically.
LICENSE: This program is protected under the apache 2.0 License, Respect it.
----


These numbers can be generated in two ways. 
  - generating to fill in trailing zeros. For example if the number is 1234567000, it will check 1234567001, 1234567002, 1234567003 and so on till it hits 1234567999.
  - generating from a text file in the format 0000000000 in phonenumbers.txt. It will go through each number till it hits the last number on the list.
----
features
  - supports asyncio threading with optional delay.
  - gets data from [https://www.reversephonelookup.com/](https://www.reversephonelookup.com/) (this website is relitivly reliable when it comes to accurate phone info however not all are accurate)
  - gets name, address, carrier type and saves to text file within data directory
  - sorts AT&T into seperate file called AT&T_data.txt and other carriers into file called non_AT&T_data.txt

features i might add if i can be asked
  - proxy rotating for 403 status codes that cant be fixed with a simple header update
  - verification with another phone lookup website
  - name/address lookup (to get furthered info on the people found)
----
this is a simulated example

https://github.com/3022-2/numberinfo/assets/82278708/8a4ea9d1-e798-44a0-b093-1fc3ae977196





```console
# How to Install & run

# Clone the repo
$ git clone https://github.com/3022-2/numberinfo.git

# watch the video guide and set headers

# install the requirements
$ pip install -r ./requirements.txt

# if ./requirements.txt doesnt work manually install the libraries 

# run script
$ python main.py

```
credit to song in video guide: [here](https://www.youtube.com/watch?v=H_d42ZSB7Pg)

[Click here to watch the video guide](https://vimeo.com/924837860)

## Legal Compliance and Responsible Use

It's important to note that while this tool utilizes web scraping to gather information, the website's terms of use may not explicitly address this method of data collection. As such, it's crucial for users to ensure that their use of this tool complies with all applicable laws and regulations regarding web scraping, data privacy, and unauthorized access to websites.
Web scraping activities can sometimes fall into legally gray areas, and misuse of this tool could potentially lead to legal consequences. Therefore, users are strongly advised to use this tool responsibly and ethically, respecting the rights of website owners and adhering to all relevant legal requirements.
By using this tool, you agree to assume full responsibility for your actions and to comply with all applicable laws and regulations in your jurisdiction. The creator of this tool shall not be held liable for any misuse or illegal activities conducted by users.
If you have any questions or concerns about the legal implications of web scraping or the use of this tool, it is recommended to seek legal advice from a qualified professional.


contact: 3011889@proton.me

"halal gotye has cured my schizophrenia"
