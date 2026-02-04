import requests

API_KEY = "METTI_LA_TUA_API_KEY"

BASE_URL = "http://api.aviationstack.com/v1/flights"


def get_flight(flight):

    params = {
        "access_key": API_KEY,
        "flight_iata": flight
    }

    r = requests.get(BASE_URL, params=params)

    data = r.json()

    if "data" not in data or not data["data"]:
        return None

    f = data["data"][0]

    info = {
        "status": f["flight_status"],
        "from": f["departure"]["airport"],
        "to": f["arrival"]["airport"],
        "dep_time": f["departure"]["scheduled"],
        "arr_time": f["arrival"]["scheduled"]
    }

    return info


if __name__ == "__main__":

    flight = input("Enter flight number (ex: FR1234): ")

    result = get_flight(flight)

    if result:
        print("✈️ Flight info:")
        for k, v in result.items():
            print(k, ":", v)
    else:
        print("Flight not found ❌")
