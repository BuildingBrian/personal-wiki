# Offline attempt 1: stopped, not valid evidence

Started 2026-09-29 16:33 with Wi-Fi off. Help, status and the start of the forced Pac-Man ingestion ran offline
(see `session.txt`, sections 0 to 3). Wi-Fi came back on during the ingestion, so the ingestion report and the
first two ask tests were recorded as `network: connected`. The run was stopped at 16:40 and repeated from the
start. It is kept here as a record, and none of it is used as offline evidence.

The attempt also showed a script problem. Status saved the model card before Gemma was loaded, so memory read
"not loaded". The script now measures memory in a final status step, after the tests have loaded the model.
