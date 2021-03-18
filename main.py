import requests
from datetime import datetime, timezone
import smtplib
import time

MY_LAT = 45.533852  # Your latitude
MY_LONG = -73.515213  # Your longitude

email = "********@gmail.com"
password = "********"


def is_iss_overhead():
    # Your position is within +5 or -5 degrees of the ISS position.
    # The current position of the ISS

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LONG + 5 >= iss_longitude >= MY_LONG - 5 and MY_LAT + 5 >= iss_latitude >= MY_LAT - 5:
        return True


def is_nighttime():
    # Sunrise and sunset times for our location
    time_now = datetime.now(timezone.utc)
    current_hour = time_now.hour

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    if current_hour > sunset or current_hour < sunrise:
        return True


while True:
    time.sleep(60)  # code will run every 60 seconds
    if is_iss_overhead() and is_nighttime():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email, to_addrs="********************@outlook.com", msg="Subject: Look up ! "
                                                                                                  "\n\n Look up the "
                                                                                                  "sky tonight as the "
                                                                                                  "ISS is crossing "
                                                                                                  "the sky over you.")
