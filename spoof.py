import socket
import time
from datetime import datetime, timezone, timedelta
import math

OTS_HOST = "192.168.1.195"
# OTS_HOST = "127.0.0.1"
OTS_PORT = 8088

def make_cot(uid, callsign, lat, lon, alt, speed, course):
    now = datetime.now(timezone.utc)
    stale = now + timedelta(seconds=60)
    fmt = "%Y-%m-%dT%H:%M:%S.000Z"
    return f'<event version="2.0" uid="{uid}" type="a-f-A-M-H-Q" time="{now.strftime(fmt)}" start="{now.strftime(fmt)}" stale="{stale.strftime(fmt)}" how="m-g"><point lat="{lat:.6f}" lon="{lon:.6f}" hae="{alt:.1f}" ce="5.0" le="3.0"/><detail><contact callsign="{callsign}"/><track speed="{speed:.2f}" course="{course:.1f}"/></detail></event>'

drones = [
    {"uid": "px4-sim-001", "callsign": "ALPHA-1", "lat": 34.0522, "lon": -117.2437},
    {"uid": "px4-sim-002", "callsign": "ALPHA-2", "lat": 34.0530, "lon": -117.2445},
]

t = 0
while True:
    for i, drone in enumerate(drones):
        lat = drone["lat"] + 0.0002 * math.sin(t + i * math.pi)
        lon = drone["lon"] + 0.0002 * math.cos(t + i * math.pi)
        alt = 100.0 + 10 * math.sin(t)
        course = (math.degrees(t) + i * 90) % 360

        msg = make_cot(drone["uid"], drone["callsign"], lat, lon, alt, 10.0, course)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((OTS_HOST, OTS_PORT))
                s.sendall(msg.encode())
                print(f"Sent CoT for {drone['callsign']}")
        except Exception as e:
            print(f"Error: {e}")

    t += 0.1
    time.sleep(1)