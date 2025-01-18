# must haves: good hospitals, open slots only, 18-44 & 45+
# good to haves: nearest shown on top


def csb():

    port = 465  # For SSL
    password = ""

    # Create a secure SSL context
    context = ssl.create_default_context()
    

    mails = ["mails as strings"]
    
    today = arrow.now().format('DD-MM-YYYY')
    pin = ["560085", "560024", "560076", "560077", "560071", "560020", "560011", "560078", "560060", "560066", "560003", "560030", "560037", "560054", "560103", "560034", "560011", "560099", "560021", "560092"]
    hospitals = ["Columbia Asia", "Aster Medcity", "Fortis Hospital", "Star Medcity Speciality Hosp", "Apollo", "Manipal", "Ramaiah", "Apollo Cradle", "St Johns", "Columbia", "Narayana", "Rainbow"]
    applic = []
    
    useragent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=560077&date=" + today
    init = requests.get(url, headers = useragent)
    
    if init.status_code == 200:
        print("connection successful")
    elif init.status_code == 400:
        sys.exit("connection unsuccessful. error code 400 (Bad Request)")
    elif init.status_code == 401:
        sys.exit("connection unsuccessful. error code 401(Unauthenticated Access)")
    elif init.status_code == 403:
        sys.exit("connection unsuccessful. error code 403 (Forbidden)")
    elif init.status_code == 500:
        sys.exit("connection unsuccessful. error code 500 (Internal Server Error)")
    else:
        sys.exit("unknown error " + str(init.status_code))
    
    
    prevfile = open("prev.txt","r")
    prev = prevfile.read()
#    print("prev:" + prev + "***")
    prevfile.close()
    
    message = ""
    for x in pin:

        response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + x + "&date=" + today, headers = useragent)
    
        n = json.dumps(response.json())
        data = json.loads(n)
    
        for i in data["centers"]:
            for item in hospitals:
                if item.lower() in i["name"].lower(): 
                    if i["sessions"][0]["available_capacity"] > 0:
                        if i["sessions"][0]["min_age_limit"] == 18:
                            age_group = "18 - 44 yrs"
                        else:
                            age_group = "45+ yrs"
                        
                        slots = str(i["sessions"][0]["available_capacity"])
                        message += "\nSlot available at " + i["name"] + "\npincode:" + x + "\nAge group:" + age_group + "\nAvailable slots:" + slots + "\ndate:" + i["sessions"][0]["date"] + "\n"
    
    prevfile = open("prev.txt","w")

    for c in prev:
        ord(c)
    for c in message:
        ord(c)
    
    if message != prev:
        for mail in mails:
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login("main_mail", password)
                server.sendmail("main_mail", mail, message)   
    
    prevfile.write(message)
#    print([ord(c) for c in message])
 #   print([ord(c) for c in prev])
        
    print(message==prev)
#    print("message:" + message)
#    print("2prev:" + prev)
    prevfile.close()
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    doc = open(r"cowindata.txt","a")
    doc.write("last run at:" + " " + current_time)
    doc.write("\n")
    doc.close()
    print("last run at:" + " " + current_time + ", " + today)

    
    
import requests
import arrow
import sys
import json
import smtplib, ssl
from datetime import datetime

csb()

