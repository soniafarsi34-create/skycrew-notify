from flask import Flask, request, render_template_string
import requests

API_KEY = "LA_TUA_API_KEY"

BASE_URL = "http://api.aviationstack.com/v1/flights"

app = Flask(__name__)

HTML = """
<html>
<head><title>SkyCrew Notify</title></head>
<body style="font-family:Arial;text-align:center">

<h2>✈️ SkyCrew Notify</h2>

<form method="post">
<input name="flight" placeholder="FR1234">
<button>Check</button>
</form>

{% if data %}
<p>Status: {{data.status}}</p>
<p>From: {{data.from_air}}</p>
<p>To: {{data.to_air}}</p>
{% endif %}

</body>
</html>
"""

def get_flight(f):

    params = {
        "access_key": API_KEY,
        "flight_iata": f
    }

    r = requests.get(BASE_URL, params=params)

    d = r.json()

    if not d.get("data"):
        return None

    f = d["data"][0]

    return {
        "status": f["flight_status"],
        "from_air": f["departure"]["airport"],
        "to_air": f["arrival"]["airport"]
    }


@app.route("/", methods=["GET","POST"])
def home():

    data = None

    if request.method=="POST":

        flight = request.form["flight"]

        data = get_flight(flight)

    return render_template_string(HTML, data=data)


app.run()
