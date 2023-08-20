import datetime
import json
import pathlib
import sys
import urllib.error
import urllib.request

url = "https://api3.hnl.info/event-ticketing/v1/hanauma_bay/events/607fcb1a9196e149ac206742/sessions/search"

today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(days=1)

payload = {
    "config": {
        "filter": {
            "event_session_starts_at": {
                "gte": today.strftime("%Y-%m-%dT10:00:00.000Z"),
                "lt": tomorrow.strftime("%Y-%m-%dT09:59:59.999Z"),
            },
        },
        "page": {
            "size": 50,
        },
        "sort": {
            "direction": 1,
            "field": "event_session_starts_at",
        },
    },
}

headers = {
    "Authorization": "Bearer eyJ4NXQiOiJNell4TW1Ga09HWXdNV0kwWldObU5EY3hOR1l3WW1NNFpUQTNNV0kyTkRBelpHUXpOR00wWkdSbE5qSmtPREZrWkRSaU9URmtNV0ZoTXpVMlpHVmxOZyIsImtpZCI6Ik16WXhNbUZrT0dZd01XSTBaV05tTkRjeE5HWXdZbU00WlRBM01XSTJOREF6WkdRek5HTTBaR1JsTmpKa09ERmtaRFJpT1RGa01XRmhNelUyWkdWbE5nX1JTMjU2IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJDQ0hOTC5ITkxcL2FodXluaEBjYXJib24uc3VwZXIiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6Imc0dlJTTVRmcDVrdXFZRkpzN0VZNm9vWW14d2EiLCJuYmYiOjE2MTkwNDc4ODksImF6cCI6Imc0dlJTTVRmcDVrdXFZRkpzN0VZNm9vWW14d2EiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvYXBpbTMuaG5sLmluZm86NDQzXC9vYXV0aDJcL3Rva2VuIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJpYXQiOjE2MTkwNDc4ODksImp0aSI6ImRhYTUwM2M0LTM4NGQtNGQ3NC1iMjQ4LWE2YTdkZjc2YzZjZSJ9.kW8HAmB8WY3PaVsDsbg0u97V0RwRCxqY_sL4s2rc_WgecWJcEtKz9yRzQi-KGpf204PGEbhNxnJNCei8FQfozjxXHaG_xsgpRwO4mWv_OccJaja2jtDdQzVKeuurvkqVR43U2B98zA1tK9pS0Yc1xuYRu3xIoSDv6RF8lZetUDS2ekNIM-mexdmJBf0l5cij8OogU_JtwJP7ixkstYeazz2QC_BoubUQWlrektQuSbELKCAadbSuL2vlMeoYTsSCi3HXw7vkw2ozZsIaG5cbSqaOaxdcdT65_eb1uV8mtOjAACPqPiSTE4CA1wR6qqJBVIseEEyxCQtEY60OE4yBUQ",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}

request = urllib.request.Request(
    data=bytes(json.dumps(payload), encoding='utf-8'),
    method="POST",
    url=url,
)

for key, value in headers.items():
    request.add_header(key, value)

try:
    response = urllib.request.urlopen(request)
except urllib.error.HTTPError as e:
    sys.stderr.write(f"{e}\n")
    sys.exit(1)
else:
    response_content = response.read()
    response_json = json.loads(response_content)
    response.close()

    data_dir = pathlib.Path(__file__).parent / "data"
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    fp = f"{data_dir / date}.json"

    with open(fp, "w") as f:
        json.dump(response_json, f)

    sys.exit(0)
