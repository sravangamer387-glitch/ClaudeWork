# BioWatt concept
Microbial fuel cells turn the chemical energy of organic matter (soil, wastewater, plant root exudates) into electricity through electroactive bacteria on an anode. Power density is low (micro- to milliwatts per cell) and voltage is about 0.3-0.7 V per cell, which is why a boost harvester with MPPT is needed.

**Use:** power a soil/water sensor tag in a vertical-farm tray or a paddy field without batteries to swap; log redox/electrode voltage as an indicator of microbial activity; teaching tool for bio-electronics.

**Design rules learnt from the budget model:** (1) put the MFC's maximum-power voltage (about half of Voc) well above the harvester's cold-start threshold; (2) budget the sleep power first (it can exceed the harvest); (3) transmit rarely, in bursts, from a storage element; (4) use a low-power radio (BLE advert, LoRa) rather than WiFi; (5) measure your own cell: a polarisation sweep (resistor box from 100 kohm down to 100 ohm) gives Voc, Rint and Pmax, which replace every assumption in `sim/budget.py`.

**Non-goals:** powering pumps, lights or WiFi tray controllers; grid-tied generation.
