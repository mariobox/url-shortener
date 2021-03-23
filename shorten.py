#import the pyhton modules we will need to make this work
import requests
import os

# get authorization token (stored for safety as an environmental variable)
token = os.environ['BITLY_TOKEN']

# ask user for the url they want to shorten
long_url = input("Input long URL: ")

# store our credential in dictionary format
headers = {
    "Authorization": token,
    'Content-Type': 'application/json',
    }

# get the group UID associated with the account (required by bitly)
groups_res = requests.get("https://api-ssl.bitly.com/v4/groups", headers=headers)
if groups_res.status_code == 200:
    # if response is OK, get the GUID
    groups_data = groups_res.json()['groups'][0]
    guid = groups_data['guid']
else:
    print("[!] Cannot get GUID, exiting...")
    exit()

# parameter to be passed with our post request
data = { "long_url": long_url, "domain": "bit.ly", "group_guid": guid }

# create our post request
response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, json=data)

# get the shortened url from the response object
short_url = response.json().get('link')

# print the short link to the console
print(f"Your short link is: {response.json().get('link')}")

# store the long url with its shortened version in a database, in this case a csv file
f = open('urls.csv', 'a')
f.write(f"{long_url},{short_url}\n")
f.close