import requests
import time

# ====== CONFIG ======
API_KEY = "e6aeec4548e487f0169847b8e5da9952"
TELEGRAM_TOKEN = "8450455745:AAFcZ-vgpo8fPh0LoZLepPjU4quGCqHOR7w"
CHAT_ID = "0"

CHECK_EVERY = 120  # secondi

# ====================

BASE_URL = "http://api.aviationstack.com/v1/flights"

WATCHED_FLIGHTS = [
    "FR1234",
    "FR4321"
]

LAST_STATUS = {}


def send_telegram(msg):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    requests.post(url, data=data)


def get_status(flight):

    params = {
        "access_key": API_KEY,
        "flight_iata": flight
    }

    r = requests.get(BASE_URL, params=params)

    d = r.json()

    if not d.get("data"):
        return None

    return d["data"][0]["flight_status"]


def check():

    for f in WATCHED_FLIGHTS:

        s = get_status(f)

        old = LAST_STATUS.get(f)

        if s and old != s:

            msg = f"✈️ {f} status: {s}"

            send_telegram(msg)

            LAST_STATUS[f] = s


print("SkyCrew Notify started ✈️")

while True:

    check()

    time.sleep(CHECK_EVERY)
