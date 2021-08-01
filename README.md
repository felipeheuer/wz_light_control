# Integration Between Warzone Events and HomeAssistant

This script will allow you to generate any sort of actions on your HomeAssistant based on events from the game Warzone.
With this you can make any smart stuff (such as light, sockets, sound system, etc) do something after a kill or death on the game.
You can even send a notification to you mom's phone after you win a match!

## Pre-Requisites
What you'll need to make it work:
- Warzone installed
- A GeForce graphics card
- GeForce Experience installed
- NVidia Highlights enabled for Warzone
- Python 3
- A HomeAssistant running somewhere (same computer or remotelly)

## Setting up
#### Script
- Just extrat the files to some folder on your computer.
- Edit `config.py`, modifying it with your HomeAssistant IP and Port. Leave the events you want to monitor into the list `wzEventsToWatch`.

#### HomeAssistant
You should have MQTT integration installed and working, then just create one sensor with the following data:
```
- platform: mqtt
  name: "WZ Lights"
  state_topic: "wz/commands/action"
  force_update : True
```

## How it works
The script will wait for the game to run. While it's running it will keep one eye into some files from NVidia Highlights that stores the last events from your match.
If the event is on the `wzEventsToWatch` list, it will shoot a MQTT package to your HomeAssistant with the event as payload.
From there you need at least one automation that checks the `WZ Lights` status and run some actions on any of your smart stuff.
