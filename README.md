# LogRaven

## Purpose:
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
- *important* I need to set up a VM to sandbox that will produce fake traffic since I am not receiving 'new' traffic from my configuration or logs
- Sending logs into analyzer for grading and cross referencing
- Determining how to grade and analyze logs depending on HEALTH, ABNORMALITIES and VULNs
- Analyzer class structure
- Connecting my analyzer to my UI structure through the information center

Future:
- Using AI to grade the severity of the cross referenced logs
- RESTFUL API integration
- Deploy-able on three different types of environments: cloud, docker and on-premise(localized)
- Searching within log storage for specific events