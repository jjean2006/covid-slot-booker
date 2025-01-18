# must haves: good hospitals, open slots only, 18-44 & 45+
# good to haves: nearest shown on top

import os
import requests
import arrow
import sys
import json
import smtplib, ssl
from datetime import datetime


port = 465  # For SSL
password = ""

# Create a secure SSL context
context = ssl.create_default_context()
    

mails = ["mails as strings"]
    
today = arrow.now().format('DD-MM-YYYY')
state = ["276", "265", "294"]
hospitals = ["Columbia Asia", "Aster Medcity", "Fortis Hospital", "Star Medcity Speciality Hosp", "Apollo", "Apollo Hospital Sheshadripuram", "St Marthas", "St Philomena", "Manipal", "Ramaiah", "Apollo Cradle", "St Johns", "Columbia", "Narayana", "Rainbow", "Vikram", "Sparsh"]
applic = []
    
useragent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
    
prevfile = open("prev.txt", "r")
prev = prevfile.read()
prevfile.close()

message = ""
flag = False
for x in state:

    response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + x + "&date=" + today, headers = useragent)
    if response.status_code == 200:
       print("connection successful")
    else:
       print("unknown error " + str(init.status_code))
       sys.exit("unknown error " + str(init.status_code))
    n = json.dumps(response.json())
    data = json.loads(n)
    
    for i in data["centers"]:
#        for item in hospitals:
#            if item.lower() in i["name"].lower():
        if (i["sessions"][0]["available_capacity"] > 0) and (i["name"] not in prev):
            if i["sessions"][0]["min_age_limit"] == 18:
                age_group = "18 - 44 yrs"
            else:
                age_group = "45+ yrs"
            flag = True
            pincode = str(i["pincode"])
            slots = str(i["sessions"][0]["available_capacity"])
            message += "\nSlot available at " + i["name"] + "\npincode:" + pincode + "\nAge group:" + age_group + "\nAvailable slots:" + slots + "\ndate:" + i["sessions"][0]["date"] + "\n"
            prev += "\nSlot available at " + i["name"] + "\npincode:" + pincode + "\nAge group:" + age_group + "\nAvailable slots:" + slots + "\ndate:" + i["sessions"][0]["date"] + "\n"

print ("MESSAGE***:", message)
if flag == True:
    print("Sending mail")
    for mail in mails:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("main_mail", password)
            server.sendmail("main_mail", mail, message)
    os.remove("prev.txt")
    prevfile = open("prev.txt","w")           
    prevfile.write(prev)
    
    prevfile.close()
    
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("last run at:" + " " + current_time + ", " + today)
