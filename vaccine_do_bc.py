import requests
from pygame import mixer 
from datetime import datetime, timedelta
import time
import discord_notify as dn
import urllib

district_id = 770
notifier = dn.Notifier("https://discord.com/api/webhooks/852952393792487434/AdckIJy5IPh0_TW0z7WNGB77Kmv-7VNLsJezFpIr8WbBmyYruGCpRGTCyxiDrKayh58-")

age = 20
pincodes = ["273402"]
num_days = 5

print_flag = 'Y'

print("Initiating Vaccine Bot.")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]
notifier.send("I am alive now!")
while True:
    counter = 0   
    s=''

    for given_date in actual_dates:

        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(district_id, given_date)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
        
        result = requests.get(URL, headers=header)

        if result.ok:
            
            response_json = result.json()
            print(response_json)        
            for session in response_json["sessions"]:
                if (session["min_age_limit"] <= age and session["available_capacity"] > 0 and session["available_capacity_dose1"]>0 ) :
                    
                    s += '{} Vaccine available at {} @ {} on {}\n'.format(session['vaccine'], session['name'], session['pincode'], session['date'])                    
                    counter += 1
        else:
            print("No Response from cowin server!")
            
    if (counter == 0):
        print("@ {}:Lawde ka government hai, koi slot nahi hai.".format(datetime.now()))
        dt = datetime.now() + timedelta(seconds=10);
    else:
        notifier.send("{} slots found!".format(counter), print_message=True)
        print(s)
        for (i,a) in enumerate(s.splitlines()):
            if(i > 10):
                notifier.send("And many more...")
                break
            try:
                notifier.send(a)
            except urllib.error.HTTPError as h:
                time.sleep(2);
        dt = datetime.now() + timedelta(minutes=30);

    while datetime.now() < dt:
        time.sleep(10)