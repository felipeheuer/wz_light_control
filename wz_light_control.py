from time import sleep
import os
from lib import wzMonitor
from lib import mqtt as hassio_mqtt
from lib import config
from lib import timeout
from lib import debug

def start_wz_monitor():
    if config.wzHighlightsPath is None:
        config.wzHighlightsPath = os.getenv('LOCALAPPDATA') + "/NVIDIA Corporation/NVIDIA Share/Highlights/"
    wz_mon = wzMonitor.wzHighlightsMonitor(config.wzHighlightsPath, "HighlightTracker.json")
    print("Waiting WZ to start (press CTRL+C to cancel)...")
    while not wz_mon.wzIsRunning():
        sleep(2)
    print("Go!")
    wz_hassio = hassio_mqtt.mqtt_hassio(config.wzHassioIpAddress, config.wzHassioPort, config.wzHassioMQTTTopic)
    debug.dbgPrint(config.wzHassioIpAddress, config.wzHassioPort, config.wzHassioMQTTTopic)

    while 1:
        last_event = None
        # wait WZ to run
        try:
            last_event = wz_mon.run()
            if last_event is None:
                break

            if last_event in config.wzEventsToWatch:
                wz_hassio.send_last_event(last_event)
                print(last_event)
            sleep(0.5)
        except:
            break
    wz_hassio.good_bye()
    print("End")

if __name__ == "__main__":
    try:
        start_wz_monitor()
    except:
        pass
