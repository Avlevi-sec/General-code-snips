#This tool allows you to search for user's ID and seat ID.
#you can also use fullsearch to print out user's full reservation history information 

import requests
import os
import sys
from pprint import pprint
from art import *

def search(user):
	url1 = f"https://api.robinpowered.com/v1.0/organizations/[org number]/users?query={user}" # insert user ID or query=username
	key = os.environ.get("robin_api_key")
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response1 = requests.request("GET", url1, headers=headers)
	user_id = response1.json()['data'][0]['id']

	url2 = f"https://api.robinpowered.com/v1.0/reservations/seats/?user_ids={user_id}&include_disabled_seats=false" #insert user ID
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response2 = requests.request("GET", url2, headers=headers)
	seat_id = response2.json()['data'][0]['seat_id']

	print(f"{user}'s user id is {user_id} and the seat id is {seat_id}")

def full_search(user):
	url1 = f"https://api.robinpowered.com/v1.0/organizations/[org number]/users?query={user}" # insert user ID or query=username
	key = os.environ.get("robin_api_key")
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response1 = requests.request("GET", url1, headers=headers)
	user_id = response1.json()['data'][0]['id']

	url2 = f"https://api.robinpowered.com/v1.0/reservations/seats/?user_ids={user_id}&include_disabled_seats=false" #insert user ID
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response2 = requests.request("GET", url2, headers=headers)
	
	pprint(response2.json())

Art=text2art("Robin Finder")
print(Art)
if sys.argv[1] == "search" and len(sys.argv) < 4:
	search(sys.argv[2])
elif sys.argv[1] == "fullsearch" and len(sys.argv) < 4:
	full_search(sys.argv[2])
else:
	print("Please enter username followed by function name such as search or fullsearch, try again")
	exit()

