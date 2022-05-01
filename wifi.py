import wifi

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

def wifi_setup():
    print("Connecting to %s" % secrets["ssid"])
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print("Connected to %s!" % secrets["ssid"])
