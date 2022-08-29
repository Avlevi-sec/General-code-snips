#The snippet lets you assign a seat using robin's API automatically for Mondays and Wednesdays. feel free to edit it.

import requests
import os
from dateutil.rrule import rrule, DAILY, MO, WE
import datetime as dt
from datetime import timedelta
import json

#Generate Robin's API token
def get_token():
	url = "https://api.robinpowered.com/v1.0/auth"
	key = os.environ.get("robin_api_key")
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response = requests.request("GET", url, headers=headers)
	print(response.text)

#Get Organization name
def get_org ():
	url = "https://api.robinpowered.com/v1.0/organizations/[org number]" #insert org number
	key = os.environ.get("robin_api_key")
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response = requests.request("GET", url, headers=headers)
	print(response.text)

#get location info
def get_locations():
	url = "https://api.robinpowered.com/v1.0/organizations/[org number]/locations?query=[location name]"#insert location name with URL encoding
	key = os.environ.get("robin_api_key")
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response = requests.request("GET", url, headers=headers)
	print(response.text)

#get users information via user ID or username
def get_users():
	url = "https://api.robinpowered.com/v1.0/organizations/[org number]/users?ids={user ID}" # insert user ID or query=username
	key = os.environ.get("robin_api_key")
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response = requests.request("GET", url, headers=headers)
	print(response.text)

#get user's seat reservation information
def get_user_seat():
	url = "https://api.robinpowered.com/v1.0/reservations/seats/?user_ids=1672244&include_disabled_seats=false" #insert user ID
	key = os.environ.get("robin_api_key")
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response = requests.request("GET", url, headers=headers)
	print(response.json())

#get seat's reservation info via reservation ID
def get_reservation():
	url = "https://api.robinpowered.com/v1.0/reservations/seats/{reservation ID}" #insert ID of reservation
	key = os.environ.get("robin_api_key")
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response = requests.request("GET", url, headers=headers)
	print(response.text)

#set specific seat to user in specific date & time
def set_seat(dt, seat_id, user_id):
	url = f"https://api.robinpowered.com/v1.0/seats/{seat_id}/reservations" #insert seat ID
	key = os.environ.get("robin_api_key")
	payload = {
	    "start": {
	        "date_time": dt + "T04:00:00Z",
	        "time_zone": "UTC"
	    },
	    "end": {
	        "date_time": dt + "T16:00:00Z",
	        "time_zone": "UTC"
	    },
	    "reservee": {"user_id": f"{user_id}"},
	    "type": "hoteled",
	    "reserver_id": f"{user_id}"
	}
	headers = {
	    "Accept": "application/json",
	    "Content-Type": "application/json",
	    "Authorization": "Access-Token " + key
	}

	response = requests.request("POST", url, json=payload, headers=headers)
	if response.json()["meta"]["status_code"] == "200":
		print(f"seat assigned sucessfully")
		return True
	else:
		print(f"seat already assigned for {dt}")
		return False



# gets all Mondays and Wedensdays of the month, remember to check the last day of the month
def get_all_dates():
	lst_dates = []
	results = rrule(DAILY,
        dtstart = dt.datetime.today(),
        until = dt.datetime.today() + timedelta(days=30),
        byweekday = (MO, WE),
)
	for result in results:
		lst_dates.append(str(result.date()))
	return lst_dates[::-1]


#starting point of program
all_dates_lst = get_all_dates()
with open('robin_users.txt', 'r') as handle:
    parsed = json.load(handle)

for user in parsed:
	user_id = str(parsed[f"{user}"]["user_id"])
	seat_id = str(parsed[f"{user}"]["seat_id"])
	for date in all_dates_lst:
		print(f"setting seat for {user} at {date}")
		set_seat(date, seat_id, user_id)
	print(f"All dates assigned for {user}")

print("\nprogram ended")
