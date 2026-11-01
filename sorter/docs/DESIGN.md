# SORTER design notes
**Timing model.** Fire distance = cam_to_pick - lead. lead = v_belt x t_latency (camera-to-decision + actuator). Because the tracker works in belt steps, v_belt may vary; but lead is a distance, so choose it for the *maximum* belt speed (or compute it from the live speed). The picker must reach the item within the 10 mm window; a late poll is a miss, never a late action (a late pick can crush the next item).
**Capacity.** 16 items in flight: belt length between camera and pick station / item pitch must be below 16.
**Pick/reject.** SR_PICK_A / SR_PICK_B map to two reject chutes or two pick positions; SR_PASS lets the item continue.
**Fin-Ray finger.** Two tapering side walls and 7 alternating diagonal ribs; the ribs shear when the finger is pushed so the tip curls toward the object. Rib count and thickness set stiffness.
