# LogRaven

## Purpose:
Currently LogRaven is designed to be a tool that collects logs from a agent-level, system-level, and service-level. 
I have setup multithreading to be able to "watch" logs that are being read in as processes from my subclasses.


## Goal:
LogRaven is an Open Source SIEM designed to be deployable in a local space, containerized space(Docker) and a cloud space.
Currently, this SIEM will be focusing on watching and interpreting logs from various sources. In the future, I plan
to be able to create cross-referencing between log types allowing more validation and reliability. 


## Features
Current:
- Setup of file structure
- Log ingestion architecture
- MVCS design structure
- Observer/Registry design pattern
- Orchestrator design pattern
- Dataclasses for log collectors
- Internal logging
- Base Unittests without implementation

In-progress:
- TBD

Future:
- *important* I need to set up a VM to sandbox that will produce fake traffic since I am not receiving 'new' traffic from my configuration or logs
- Sending logs into analyzer for grading and cross referencing
- Determining how to grade and analyze logs depending on HEALTH, ABNORMALITIES and VULNs
- Analyzer class structure
- Connecting my analyzer to my UI structure through the information center