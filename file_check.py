from lib import wzMonitor
from time import sleep

# eventsToWatch=["Bonk","Collateral","Frenzy Kill","Fury Kill","Juggernaut","Kill Chain","Mega Kill","Merciless","Nuke","Popcorn","Regicide","Relentless","Stick","Super Kill","Ultra Kill","Warzone Backstabber","Warzone Death","Warzone Double Kill","Warzone Down","Warzone Elimination","Warzone Longshot","Warzone Revenge","Warzone Surgical","Warzone Triple Kill","Warzone Win"]
eventsToWatch=["Warzone Death","Warzone Double Kill","Warzone Down","Warzone Elimination","Warzone Revenge","Warzone Triple Kill","Warzone Win"]

# possible processes name. To test
# modernwarfare.exe
# Call of Duty: Modern Warfare 2019
# call_of_duty_modern_warfare_2019

wz_mon = wzMonitor.wzHighlightsMonitor("C:/Users/felip/AppData/Local/NVIDIA Corporation/NVIDIA Share/Highlights/", "HighlightTracker.json", False)
# wz_mon = wzMonitor.wzHighlightsMonitor("test_files/", "HighlightTracker.json", True)
# wz_mon = wzMonitor.wzHighlightsMonitor("test_files/", "simple.json")
# wz_mon = wzMonitor.wzHighlightsMonitor("test_files/", "test.txt")

while 1:
    lastEvent = None
    try:
        lastEvent = wz_mon.run()
        if lastEvent is not None and lastEvent in eventsToWatch:
            print (lastEvent)
        else:
            break
        sleep(0.5)
    except:
        break
print("End")