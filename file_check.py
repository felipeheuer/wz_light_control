from lib import wzMonitor

wz_mon = wzMonitor.wzHighlightsMonitor("C:/Users/felip/AppData/Local/NVIDIA Corporation/NVIDIA Share/Highlights/", "HighlightTracker.json")
# wz_mon = wzMonitor.wzHighlightsMonitor("test_files/", "HighlightTracker.json")
# wz_mon = wzMonitor.wzHighlightsMonitor("test_files/", "simple.json")
# wz_mon = wzMonitor.wzHighlightsMonitor("test_files/", "test.txt")
wz_mon.run()
